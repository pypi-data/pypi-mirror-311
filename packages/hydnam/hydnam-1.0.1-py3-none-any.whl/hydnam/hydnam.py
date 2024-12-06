import math
from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from hydnam.columns_constants import TIMESERIES, INTERVAL, TEMPERATURE, PRECIPITATION, EVAPOTRANSPIRATION, DISCHARGE
from hydnam.dataset import Dataset
from hydnam.parameters import Parameters
from hydnam.simulation_result import SimulationResult
from hydnam.statistics import Statistics


def validate_time_series(df: pd.DataFrame):
    if not df[TIMESERIES].is_monotonic_increasing:
        raise ValueError("The time series is not strictly increasing.")

    time_diffs = df[TIMESERIES].diff().dropna()
    if not time_diffs.nunique() == 1:
        raise ValueError("The intervals between datetimes are not consistent.")


def validate_columns_data(df: pd.DataFrame):
    for column in df.columns:
        if df[column].isnull().any():
            raise ValueError(f"The column '{column}' contains missing data. Please ensure all columns are filled.")


class HydNAM:
    def __init__(
            self,
            dataset: Dataset,
            parameters: Parameters,
            area: float,
            interval: float = 24.0,
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            spin_off: float = 0.0,
            ignore_snow: bool = True,
    ):
        self._dataset = dataset
        self._parameters = parameters
        self._area = area
        self._interval = interval
        self._flow_rate = self._area / (3.6 * self._interval)
        self._start = start
        self._end = end
        self._spin_off = spin_off
        self._ignore_snow = ignore_snow

        self._statistics = Statistics()
        self._simulation_result = SimulationResult()

        self._run_model(opz=False)

    @property
    def dataset(self) -> Dataset:
        return self._dataset

    @property
    def parameters(self) -> Parameters:
        return self._parameters

    @property
    def area(self) -> float:
        return self._area

    @property
    def interval(self) -> float:
        return self._interval

    @property
    def start(self) -> datetime:
        return self._start

    @property
    def end(self) -> datetime:
        return self._end
    
    @property
    def spin_off(self) -> float:
        return self._spin_off
    
    @property
    def ignore_snow(self) -> bool:
        return self._ignore_snow

    @property
    def statistics(self) -> Statistics:
        return self._statistics

    @property
    def simulation_result(self) -> SimulationResult:
        return self._simulation_result

    def _validate_interval(self, df: pd.DataFrame):
        df = df.copy()
        df[INTERVAL] = df[TIMESERIES].diff()
        interval_hours = pd.Timedelta(hours=self._interval)
        is_valid_interval_hours = df[INTERVAL].dropna().eq(interval_hours).all()
        if not is_valid_interval_hours:
            raise ValueError(f"The intervals between datetimes are not consistent. Require: {self._interval}")
        df = df.drop(columns=[INTERVAL])
        return df

    def _filter_timeseries(self, df: pd.DataFrame):
        df = df.copy()

        start = self._start
        end = self._end

        if not pd.api.types.is_datetime64_any_dtype(df[TIMESERIES]):
            raise ValueError("The TIME_SERIES column must be of datetime type.")

        min_time = df[TIMESERIES].min()
        max_time = df[TIMESERIES].max()

        if start is not None and (start < min_time or start > max_time):
            raise ValueError("The 'start' parameter is out of the DataFrame's time range.")

        if end is not None and (end < min_time or end > max_time):
            raise ValueError("The 'end' parameter is out of the DataFrame's time range.")

        if start is not None and end is not None and end < start:
            raise ValueError("The 'end' parameter cannot be earlier than the 'start' parameter.")

        if start is None and end is None:
            return df
        elif start is None:
            return df[df[TIMESERIES] <= end]
        elif end is None:
            return df[df[TIMESERIES] >= start]
        else:
            return df[(df[TIMESERIES] >= start) & (df[TIMESERIES] <= end)]

    def _validate_dataset_n_provide_dataframe(self):
        df = self._dataset.to_dataframe()
        validate_columns_data(df)
        validate_time_series(df)
        df = self._validate_interval(df)
        return df

    def _compute_nam(self, x):
        self._parameters.from_params(x)
        print(f"Calculating with parameters: {self._parameters}")
        sr = self._simulation_result

        qofmin, beta, pmm, carea = 0.4, 0.1, 10, 1.0
        interval = self._interval
        states = np.array([0, 0, 0.9 * x[1], 0, 0, 0, 0, 0.1])
        snow, u, _l, if1, if2, of1, of2, bf = states

        umax, lmax, cqof, ckif, ck12, tof, tif, tg, ckbf, csnow, snowtemp = x[:11]
        ckif /= interval
        ck12 /= interval
        ckbf /= interval

        lfrac = _l / lmax
        fact = self._flow_rate

        q_sim = np.zeros(sr.P.size)
        l_soil, u_soil, s_snow, q_snow = (np.zeros(sr.P.size) for _ in range(4))
        q_inter, e_eal, q_of, q_g, q_bf = (np.zeros(sr.P.size) for _ in range(5))

        for t, (prec, evap, temp) in enumerate(zip(sr.P, sr.E, sr.T)):
            if temp < snowtemp:
                snow += prec
                qs = 0
            else:
                qs = min(csnow * temp, snow)
                snow -= qs

            u1 = u + (prec + qs) if temp >= 0 else u
            eau = min(u1, evap)
            eal = (evap - eau) * lfrac if u1 > evap else 0

            u2 = min(u1 - eau, umax)
            qif = (lfrac - tif) / (1 - tif) * u2 / ckif if lfrac > tif else 0
            u3 = u1 - eau - qif
            pn = max(0, u3 - umax)
            u = min(u3, umax)

            n = int(pn / pmm) + 1
            pnlst = pn - (n - 1) * pmm
            eal /= n

            qofsum, gsum = 0, 0
            for i in range(n):
                pn = pmm if i < n - 1 else pnlst
                qof = cqof * (lfrac - tof) / (1 - tof) * pn if lfrac > tof else 0
                qofsum += qof
                g = (lfrac - tg) / (1 - tg) * (pn - qof) if lfrac > tg else 0
                gsum += g

            c = np.exp(-1. / ckbf)
            bf = bf * c + gsum * carea * (1 - c)

            c = np.exp(-1. / ck12)
            if1 = if1 * c + qif * (1 - c)
            if2 = if2 * c + if1 * (1 - c)

            of = 0.5 * (of1 + of2) / interval
            ckqof = ck12 * (of / qofmin) ** (-beta) if of > qofmin else ck12
            c = np.exp(-1. / ckqof)
            of1 = of1 * c + qofsum * (1 - c)
            of2 = of2 * c + of1 * (1 - c)

            if t >= self._spin_off:
                q_sim[t] = fact * (if2 + of2 + bf)
                l_soil[t], u_soil[t] = lfrac, u
                s_snow[t], q_snow[t] = snow, qs
                q_inter[t], e_eal[t] = qif, eal
                q_of[t], q_g[t], q_bf[t] = qofsum, gsum, bf

                dl = pn - qofsum - gsum
                _l = min(_l + dl - eal, lmax)
                lfrac = _l / lmax

        sr.Q_sim = q_sim
        sr.L_soil = l_soil
        sr.U_soil = u_soil
        sr.S_snow = s_snow
        sr.Q_snow = q_snow
        sr.Q_inter = q_inter
        sr.E_eal = e_eal
        sr.Q_of = q_of
        sr.Q_g = q_g
        sr.Q_bf = q_bf

        self._stats()
        print(f"Statistics: {self.statistics}")
        print("-" * 10)

    def _init_input(self, df: pd.DataFrame):
        sr = self._simulation_result
        sr.timeseries = df[TIMESERIES].reset_index(drop=True)
        sr.T = df[TEMPERATURE].reset_index(drop=True)
        sr.P = df[PRECIPITATION].reset_index(drop=True)
        sr.E = df[EVAPOTRANSPIRATION].reset_index(drop=True)
        sr.Q_obs = df[DISCHARGE].reset_index(drop=True)
        sr.Q_sim = pd.Series(0.0, index=range(df.size))
        sr.L_soil = pd.Series(0.0, index=range(df.size))

    def _stats(self):
        sr = self._simulation_result
        stats = self._statistics
        mean = np.mean(sr.Q_obs)
        stats.nse = 1 - (sum((sr.Q_sim - sr.Q_obs) ** 2) /
                         sum((sr.Q_obs - mean) ** 2))
        stats.rmse = float(np.sqrt(sum((sr.Q_sim - sr.Q_obs) ** 2) / len(sr.Q_sim)))
        stats.fbias = (sum(sr.Q_obs - sr.Q_sim) / sum(sr.Q_obs)) * 100

    def _objective(self, x):
        sr = self._simulation_result
        self._compute_nam(x)
        n = math.sqrt((sum((sr.Q_sim - sr.Q_obs) ** 2)) / len(sr.Q_obs))
        return n

    def _run_model(self, opz: bool = False):
        df = self._validate_dataset_n_provide_dataframe()
        df = self._filter_timeseries(df)
        self._init_input(df)

        params = minimize(
            self._objective,
            self._parameters.to_initial_params(),
            method='SLSQP',
            bounds=self._parameters.get_bounds(self._ignore_snow),
            options={
                'maxiter': 1e8, 'disp': True, 'eps': 0.01
            }
        ).x if opz else self._parameters.to_initial_params()

        self._compute_nam(params)

    def optimize(self):
        self._run_model(opz=True)

    def set_parameters(self, parameters: Parameters):
        self._parameters = parameters
        self._run_model(opz=False)

    def __str__(self):
        return f"""HydNAM 🍃 🌧 ☔ 💦
FROM: {self.simulation_result.timeseries.iloc[0]}
TO: {self.simulation_result.timeseries.iloc[-1]}                
Parameters: {self._parameters}
Statistics: {self._statistics}
        """
