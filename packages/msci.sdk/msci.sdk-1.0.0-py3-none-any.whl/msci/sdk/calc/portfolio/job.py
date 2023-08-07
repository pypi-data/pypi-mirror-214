import datetime
import logging
import time

import pandas as pd

from .metrics import Metrics
from .optimizer_result import OptimizerResult
from .results import TaxOutput
from .utils.enums import CalculationTypeEnum
from .utils.job_utility import format_portfolio_output, format_dates_output


class Job:
    def __init__(self, job_id: str, get, post, calculation_type=None, profile=None):
        """
        Job control to get results, metrics, job status and other job info using the jobId.
        """
        self.start_time = datetime.datetime.now()
        self.job_id = job_id
        self.get = get
        self.post = post
        self.calculation_type = calculation_type
        self.profile = profile
        self.logger = logging.getLogger(__name__)

    def wait(self):
        """
        Wait for the job to get completed. It will check the status every 5 secs.
        """
        fullstatus = self.status()
        waitsec = 5
        if self.calculation_type:
            is_simulation = self.calculation_type == CalculationTypeEnum.SIMULATION
        else:
            is_simulation = False
        while fullstatus["status"] in ["running", "queued"]:
            waittime = datetime.datetime.now() - self.start_time
            if is_simulation and fullstatus["status"] == 'running':
                p = fullstatus['percentDone'] / 100
                ldate = fullstatus["latestValuationDate"]
                if p > 0.0:
                    timeleft = waittime * ((1 - p) / p)
                    self.logger.info(
                        f"{p * 100}% done, completed {ldate}, elapsed time {waittime}, estimated {timeleft} left.")
                else:
                    self.logger.info(f"{p * 100}% done, completed {ldate}, elapsed time {waittime}")
            else:
                mystatus = fullstatus["status"]
                self.logger.info(
                    f"Waiting {waittime} on job {self.job_id} with status {mystatus}, waiting {waitsec} seconds to check again")

            time.sleep(waitsec)
            fullstatus = self.status()

        totaltime = datetime.datetime.now() - self.start_time
        fullstatus = self.status()
        mystatus = fullstatus["status"]
        self.logger.info(f"Completed job {self.job_id} with status {mystatus} in {totaltime}")
        return fullstatus

    def get_metrics(self):
        """
        Retrieve all the metrics computed by a job. It can be used while the job status is running, or when completed.
        """
        self.logger.debug(f"Fetching metrics for job id : {self.job_id}")
        resp = self.get(f"jobs/{self.job_id}/metrics")
        all_metrics = resp.json()
        metrics = Metrics(all_metrics)
        return metrics

    def status(self):
        """
        Retrieve the status of a job.
        """
        self.logger.debug(f"Fetching status for job id : {self.job_id}")
        resp = self.get(f"jobs/{self.job_id}/status")
        return resp.json()

    def info(self):
        """
        Retrieve the details of a job, including profile information.
        """
        self.logger.info(f"Fetching info for job id : {self.job_id}")
        resp = self.get(f"jobs/{self.job_id}/info")
        return resp.json()

    def close_portfolio_dates(self, to_dataframe: bool = True):
        """
        List dates of closing portfolios from a backtesting job.
        """
        self.logger.debug(f"Fetching dates of closing portfolios for job id : {self.job_id}")
        resp = self.get(f"jobs/{self.job_id}/closePortfolios")
        return format_dates_output(resp, to_dataframe)

    def close_portfolio_on(self, date, to_dataframe: bool = True):
        """
        Retrieve closing portfolios from a backtesting job.
        """
        self.logger.debug(f"Fetching closing portfolios for job id : {self.job_id} for date {date}")
        resp = self.get(f"jobs/{self.job_id}/closePortfolios/{date}")
        return format_portfolio_output(resp, to_dataframe)

    def open_portfolio_dates(self, to_dataframe: bool = True):
        """
        List dates of opening portfolios from a backtesting job.
        """
        self.logger.debug(f"Fetching dates of opening portfolios for job id : {self.job_id}")
        resp = self.get(f"jobs/{self.job_id}/openPortfolios")
        return format_dates_output(resp, to_dataframe)

    def open_portfolio_on(self, date, to_dataframe: bool = True):
        """
        Retrieve opening portfolios from a backtesting job.
        """
        self.logger.debug(f"Fetching opening portfolios for job id : {self.job_id} and date {date}")
        resp = self.get(f"jobs/{self.job_id}/openPortfolios/{date}")
        return format_portfolio_output(resp, to_dataframe)

    def rebalanced_portfolio_dates(self):
        """
        List dates of rebalanced portfolios from a single-day rebalance job.
        """
        self.logger.debug(f"Fetching dates of rebalanced portfolios for job id : {self.job_id}")
        resp = self.get(f"jobs/{self.job_id}/rebalancedPortfolios")
        return resp.text

    def rebalanced_portfolio_on(self, date, to_dataframe: bool = True):
        """
        Retrieve rebalanced portfolios from a single-day rebalance job.
        """
        self.logger.debug(f"Fetching rebalanced portfolios for job id : {self.job_id} and date {date}")
        resp = self.get(f"jobs/{self.job_id}/rebalancedPortfolios/{date}")
        return format_portfolio_output(resp, to_dataframe)

    def get_valuations(self):
        """
        Retrieve the portfolio value after each rebalance.
        """
        self.logger.debug(f"Get valuations for job id : {self.job_id}")
        resp = self.get(f"jobs/{self.job_id}/valuations")
        return pd.json_normalize(resp.json()["values"])

    def open_taxlots_on(self, date):
        """
        Retrieve open tax lots for given date for the last node for a (partially) completed job.
        """
        self.logger.info(f"Get open tax lots for job id : {self.job_id} and date {date}")
        resp = self.get(f"jobs/{self.job_id}/openTaxLots/{date}")
        return resp.json()

    def close_taxlots_on(self, date):
        """
        Retrieve job close tax lots for given date for the last node for a (partially) completed job.
        """
        self.logger.info(f"Get close tax lots for job id : {self.job_id} and date {date}")
        resp = self.get(f"jobs/{self.job_id}/closeTaxLots/{date}")
        return resp.json()

    def tax_output(self, **kwargs):
        """
        Retrieve TaxOutput object which contains tax related details.
        """
        return TaxOutput(self, **kwargs)

    def optimizer_result(self):
        """
        Retrieve OptimizerResult object which contains metric information for OPTIMIZER_RESULT.
        """
        metric_type = "OPTIMIZER_RESULT"
        self.logger.debug(f"Fetching {metric_type} metrics for job id : {self.job_id}")
        metrics_response = self.get(f"jobs/{self.job_id}/metrics/{metric_type}")
        return OptimizerResult(metrics_response.json())

    def trade_suggestions_on(self, date):
        """
        Retrieve the suggested trades for a job
        """
        trades_response = self.get(f"jobs/tradeSuggestions/{self.job_id}/{date}")
        return pd.json_normalize(trades_response.json()["suggestions"])
