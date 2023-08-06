from btg_investment_flow_portfolio_optimization.portfolio_optimization import (
    PortfolioOptimizer,
)

import pandas as pd
from datetime import datetime
from typing import List, Tuple

class StandardPortfolioOptimizer(PortfolioOptimizer):
    @staticmethod
    def sum_between_dates(df, start_date, end_date, quantile):
        """Calculate the sum of a quantile between two dates."""
        df.index = pd.to_datetime(df.index)
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        mask = (df.index >= start_date) & (df.index <= end_date)
        subset_df = df.loc[mask]

        # Set negative values to zero
        subset_df.loc[subset_df[quantile] < 0, quantile] = 0

        return subset_df[quantile].sum()

    def generate_time_slots(self, start_date, end_date):
        """Generate a list of intervals representing the starting and ending points of each time slot"""
        time_slots = []
        current_date = start_date

        def calculate_interval_end_and_hour(current_date: datetime, end_date: datetime, days_to_add: int, hour_if_within_period: int, hour_if_exceeds_period: int) -> Tuple[datetime, int]:
            proposed_end_date = current_date + pd.DateOffset(days=days_to_add)

            if proposed_end_date <= end_date or current_date == end_date:
                return proposed_end_date, hour_if_within_period
            else:
                return end_date, hour_if_exceeds_period

        def append_time_slot(time_slots: List[Tuple[datetime, datetime]], interval_start: datetime, start_hour: int, interval_end: datetime, end_hour: int):
            start = interval_start.replace(hour=start_hour, minute=0, second=0)
            end = interval_end.replace(hour=end_hour, minute=0, second=0)
            time_slots.append((start, end))


        if start_date.weekday() not in [0,4]:
            days_to_next_monday = (-start_date.weekday()) % 7
            days_to_next_friday =(4-start_date.weekday()) % 7
            offset = min(days_to_next_monday,days_to_next_friday)
            next_recommendation = current_date + pd.DateOffset(days=offset)
            next_recommendation_hour = 16 if days_to_next_monday > days_to_next_friday else 8
            append_time_slot(time_slots, start_date, 9, next_recommendation, next_recommendation_hour)

        while current_date <= end_date:
            if current_date.weekday() == 0:  # Monday
                interval_start = current_date
                interval_end, interval_end_hour = calculate_interval_end_and_hour(current_date, end_date, days_to_add=4, hour_if_within_period=16, hour_if_exceeds_period=16)
                append_time_slot(time_slots, interval_start, 9, interval_end, interval_end_hour)

            elif current_date.weekday() == 4:  # Friday
                interval_start = current_date
                interval_end, interval_end_hour = calculate_interval_end_and_hour(current_date, end_date, days_to_add=3, hour_if_within_period=8, hour_if_exceeds_period=16)
                append_time_slot(time_slots, interval_start, 17, interval_end, interval_end_hour)

                
            current_date += pd.DateOffset(days=1)
        return time_slots

    def optimize(self, quantile="0.5"):
        recommendations = {}

        # Convert date to datetime
        start_date = min(
            pd.to_datetime(df["quantiles"].index.min())
            for df in self.forecasts.values()
        )
        end_date = max(
            pd.to_datetime(df["quantiles"].index.max())
            for df in self.forecasts.values()
        )

        # Generate the time slots
        time_slots = self.generate_time_slots(start_date, end_date)

        # Loop through all series in forecasts
        for series_name in self.forecasts:
            # Make sure our index is a DateTimeIndex
            df = self.forecasts[series_name]["quantiles"].copy()
            df.index = pd.to_datetime(df.index)

            # Loop through all time slots
            for start_time_slot, end_time_slot in time_slots:
                # Use sum_between_dates function to sum the data within this time slot
                sum_quantile = self.sum_between_dates(
                    df, start_time_slot, end_time_slot, quantile
                )

                # Add the sum for this time slot to the recommendations
                timeslot_str = f"{start_time_slot.strftime('%A / %Y-%m-%d %H:%M:%S')} - {end_time_slot.strftime('%A / %Y-%m-%d %H:%M:%S')}"
                if timeslot_str not in recommendations:
                    recommendations[timeslot_str] = 0
                recommendations[timeslot_str] += sum_quantile

        return recommendations
