---
title: "Data"
---
> Last updated: {{ "now" | date: "%Y-%m-%d --- %H:%M:%S" (%Z)}}

This project utilizes data that is output by the Observatory on Social Media's (OSoMe) Decahose infrastructure.
- [Learn more about OSoMe](https://osome.iu.edu/)
- [Learn more about Twitter's Decahose](https://developer.twitter.com/en/docs/twitter-api/enterprise/decahose-api/overview/decahose)

Currently, the data is returned in Twitter's V1 format as this is how data is delivered by the Decahose.
You can see details on migrating from V1 and V2 [here](https://developer.twitter.com/en/docs/twitter-api/migrate/data-formats/standard-v1-1-to-v2).

The data we retrieve contains any tweet that has been indexed as containing at least one low-credibility domain.
Low-credibility domains are defined based on the [iffy.news/](iffy.news/) list, which is a curated version of [Media Bias/Fact Check](https://mediabiasfactcheck.com/) data.

Every three months, we pass a list of all [iffy.news/](iffy.news/) domains as a query for the previous month.
This will return all tweets that contain at least one of these low-credibility domains.
Then a data file is saved in the below location:
- `lisa.luddy.indiana.edu:/home/data/osome_swap/moe/jobs/top_fibers_data`

Typically, the directory will have subfolders for each month that are formatted in the below fashion:
```
drwxr-sr-x 3 truthy truthy 43 Nov 10 12:43 2022-07
drwxr-sr-x 3 truthy truthy 43 Nov 10 18:18 2022-08
drwxr-sr-x 3 truthy truthy 43 Nov 10 18:18 2022-09
drwxr-sr-x 3 truthy truthy 43 Nov 10 16:54 2022-10
```

In each of these folders, you will see the output from the [OSoMe](https://osome.iu.edu/) infrastructure which includes the tweet IDs as well as the raw tweet content.



