#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
# pylint: disable=missing-docstring

import sys
import csv

if __name__ == '__main__':
    #try:
    input_time = sys.argv[2]
    input_value = sys.argv[3]
    output_time_now = input_time.strip() + ' (Now)'
    output_value_now = input_value.strip() + ' (Now)'
    output_time_previous = input_time.strip() + ' (Previous)'
    output_value_previous = input_value.strip() + ' (Previous)'
    #except IndexError:
        #input_time = 'Time Weight (AV)           '
        #input_value = 'Weight (AV)           '
    with open(sys.argv[1], newline='') as input_file:
        data = list(csv.DictReader(input_file))
    with open(sys.argv[1].rstrip('.csv') + '.output.csv', 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=(output_time_now,
                                                         output_value_now,
                                                         output_time_previous,
                                                         output_value_previous,
                                                         'Difference'))
        writer.writeheader()
        previous_row = data[0]
        for row in data:
            difference_to_previous = float(row[input_value]) - float(previous_row[input_value])
            if difference_to_previous > 10 or difference_to_previous < -10:
                print(80 * '-')
                print('Difference:', difference_to_previous)
                print('Previous:  ', previous_row[input_time], '-', previous_row[input_value])
                print('Now:       ', row[input_time], '-', row[input_value])
                writer.writerow({output_time_now: row[input_time],
                                 output_value_now: row[input_value],
                                 output_time_previous: previous_row[input_time],
                                 output_value_previous: previous_row[input_value],
                                 'Difference': difference_to_previous})
            last_seen_row = row
