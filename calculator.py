"""
Staffing Calculator

This module provides functions to calculate the optimal number of staff based on workload, productivity, and cost.
"""

import math

def calculate_staff(required_hours, hours_per_employee):
    """
    Calculate the minimum number of staff needed given total required hours of work and hours each employee can work.
    Args:
        required_hours (float): Total hours of work required.
        hours_per_employee (float): Number of hours each employee can work.
    Returns:
        int: Minimum number of staff required.
    """
    return math.ceil(required_hours / hours_per_employee)


def calculate_cost(num_staff, hourly_rate, hours_per_employee):
    """
    Calculate the total staffing cost.
    Args:
        num_staff (int): Number of staff required.
        hourly_rate (float): Hourly rate per employee.
        hours_per_employee (float): Number of hours each employee works.
    Returns:
        float: Total cost for staffing.
    """
    return num_staff * hourly_rate * hours_per_employee


if __name__ == "__main__":
    # Example usage
    required_hours = 100
    hours_per_employee = 40
    hourly_rate = 25

    staff_needed = calculate_staff(required_hours, hours_per_employee)
    total_cost = calculate_cost(staff_needed, hourly_rate, hours_per_employee)

    print(f"Staff needed: {staff_needed}")
    print(f"Total cost: ${total_cost:.2f}")
