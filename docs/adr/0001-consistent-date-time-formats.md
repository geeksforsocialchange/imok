# Consistent Date/Time Formats

* Status: proposed
* Deciders: Kim, Alice
* Date: 2020-05-06

## Context and Problem Statement

We want to use consistent date/time formats and methods of rendering them across the whole of imok, but there are a number of options for how we do that. There are pros and cons to all of them.

## Considered Options

* Use `strftime('%x')` and `strftime('%X')` (long form dates and times in member's locale)
* Use `strftime('%Y-%m-%d')` and `strftime('%H:%M')` (ISO-8601 24hour times)
* Use `time_format(time_obj, format='SHORT_TIME_FORMAT', use_l10n=True)` and `date_format(date_obj, format='SHORT_DATE_FORMAT', use_l10n=True)` (short form dates and times in member's locale)
* Use Babel and standard dates and short-form times with the member's locale

As we are discussing both time and date formats, there is of course the option to mix and match.

## Decision Outcome

Chosen option: Do nothing.  The current mixture of formats we have are working, and this decision is not one we want to make without consultation.  We will raise a GitHub issue to discuss this in more depth.

## Pros and Cons of the Options

### Long form dates and times in member's locale

This is the method we have been mostly using up until now. It displays a long form of the date and time in a way that the member's locale describes (en_GB for admins)

Examples:

| locale | date     | time     |
|--------|----------|----------|
| *      | 05/04/21 | 18:25:27 |

* Good, because it is mostly what we have been using already
* Good, because it plays well with timezones
* Bad, because the long times with seconds are ugly and unhelpful
* Bad, because it doesn't actually use the correct locale

### ISO-8601 24hour times

Display dates in ISO-8601 and times using the 24 hour clock.

Examples:

| locale | date       | time  |
|--------|------------|-------|
| *      | 2021-05-04 | 18:25 |

* Good, because it is a standard format
* Good, because the seconds are not displayed
* Good, because dates cannot be confused once you know ISO-8601 (2020-03-02)
* Bad, because some people struggle with the 24 hour clock
* Bad, because some people struggle with ISO-8601
* Bad, because timezone support needs further testing

### Short form dates and times in member's locale

Use `time_format` and `date_format` with the `SHORT` formats.

Examples:

| locale | date       | time  |
|--------|------------|-------|
| en_GB      | 4 May 2021  | 6:46 p.m. |
| cy_GB      | 4 Mai 2021  | 6:46 y.h. |
| sq_AL      | 04 Maj 2021 | 6.46.PM   |
| ti_ER      | May 4, 2021 | 6:57 p.m. |

* Good, because the seconds are not displayed
* Good, because we assume it will be familiar to members
* Good, because it should work well with timezone support
* Bad, because developers don't read/write the supported locales so don't know if they are displayed correctly
* Bad, because coverage of locales is relatively small and it appears to fall back to en_US

### Babel and short form dates and times in member's locale

Add an additional Python module `Babel` to display the times in the member's locale but with greater language support than Django's own formats.

Examples:

| locale | date       | time  |
|--------|------------|-------|
| en_GB      | 4 May 2021  | 18:46             |
| cy_GB      | 4 Mai 2021  | 18:46             |
| sq_AL      | 4 Maj 2021  | 6:46 e pasdites   |
| ti_ER      | 04-ግን-2021  | 6:46 ድሕር ሰዓት     |

* Good, because the dates and times are truly localised
* Good, because we assume it will be familiar to members
* Bad, because it requires an extra module
* Bad, because we don't know how well it will work with timezones
* Bad, because the times are potentially verbose
* Bad, because developers don't read/write the supported locales so don't know if they are displayed correctly
