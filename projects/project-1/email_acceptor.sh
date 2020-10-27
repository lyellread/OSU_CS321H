#! /bin/bash

# Inspired by <https://stackoverflow.com/a/35924143/8704864>

# Define email regex string
EMAIL_REGEX='^[A-Za-z_.-\d]+@[A-Za-z]+\.[a-z.]+$'

# Regex Explanation
# - ^ : Start of string
# - [A-Za-z_.-\d]+ : match any number of numbers and letters and ._-
# - @ : Match a single '@'
# - [A-Za-z]+ : Match any number of upper or lowercase alphabetic characters
# - \. : Match period
# - [a-z.]+ : Match domain extension, i.e com, co.nz
# - $ : End of string

# Check args
if [ "$#" -ne 1 ]
then
	echo "Usage: ./email_acceptor.sh <email>"
	exit 2
fi

# Check email
if [[ $1 =~ $EMAIL_REGEX ]]
then
	echo "Passed Email Check"
	exit 0
else
	echo "Failed Check"
	exit 1
fi