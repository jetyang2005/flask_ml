#!/bin/bash

# Big Data Analytics Using Splunk
# By Peter Zadrozny and Raghu Kodali
# Apress, May 2013 ISBN 978-1-4302-5761-5
# Copyright (C) 2013 Peter Zadrozny and Raghu Kodali

# Chapter 9
# Download the flight data from the Transtats web site
# Until September 2012

for i in 10 11 12
do
        wget "https://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_1987_"$i".zip" --no-check-certificate
done

for i in 1988 1989 1990 1991 1992 1993 1994 1995 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017
do

        wget "https://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_"$i"_1.zip" --no-check-certificate
        wget "https://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_"$i"_2.zip" --no-check-certificate
        wget "https://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_"$i"_3.zip" --no-check-certificate
        wget "https://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_"$i"_4.zip" --no-check-certificate
        wget "https://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_"$i"_5.zip" --no-check-certificate
        wget "https://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_"$i"_6.zip" --no-check-certificate
        wget "https://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_"$i"_7.zip" --no-check-certificate
        wget "https://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_"$i"_8.zip" --no-check-certificate
        wget "https://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_"$i"_9.zip" --no-check-certificate
        wget "https://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_"$i"_10.zip" --no-check-certificate
        wget "https://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_"$i"_11.zip" --no-check-certificate
        wget "https://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_"$i"_12.zip" --no-check-certificate
done
for i in 1 2 3 4 5 6 7 8 9
do
       wget "https://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_2012_"$i".zip" --no-check-certificate
done