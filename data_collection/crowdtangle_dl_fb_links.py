"""
Purpose:
    Download Facebook posts from CrowdTangle based on a list of links.
    NOTE:
        - Requires a CrowdTangle API token
        - The data pulled is dictated by the constant variables at the top of the script.
        Particularly important are:
            - NUMBER_OF_MONTHS_TO_PULL
            - OFFSET

Inputs:
    Required:
        -d / --domains-file: Full path to a file with one domain on each line.
            Posts will be downloaded that include at least one of these domains
        -o / --out-dir: Directory where you'd like to save the output data

Outputs:
    One new-line delimited json.gz file with all posts from FB for the specified period.
    Output file name form:
        - start_date-end_date__candidate_fb_posts.json.gz
            - `start_date` and `end_date` take the following format: YYYY-MM-DD
            - Dates represent the date range of the downloaded data
            - NOTE: end_date is NOT inclusive. This means that a date range like
                2022-11-05-2022-11-06 indicates that the data was pulled for
                only 2022-11-05.
Authors:
    Matthew R. DeVerna
"""
import gzip
import json
import os
import requests
import time

from top_fibers_pkg.utils import (
    parse_cl_args_ct_dl,
    load_lines,
    get_start_and_end_dates,
)

SCRIPT_PURPOSE = (
    "Download Facebook posts from Facebook that contain domains from a list."
)

LOG_FILE_NAME = "top_fibers_fb_link_dl.log"
NUMBER_OF_MONTHS_TO_PULL = 1
NUMBER_OF_POSTS_PER_CALL = 100

# Sets the end date. Must be <= 0.
# If OFFSET = 0, end_date is last day of current month
# If OFFSET = -1, end_date is last day of previous month
OFFSET = -1

# Number of seconds to wait before every query, regardless of success or error
WAIT_BTWN_POSTS = 8

# Base number of seconds to wait after encountering an error, raised to the number of try counts
WAIT_BTWN_ERROR_BASE = 2


def ct_get_search_posts(
    count=100,
    start_time=None,
    end_time=None,
    include_history=None,
    sort_by="date",
    types=None,
    search_term=None,
    account_types=None,
    min_interactions=0,
    offset=0,
    api_token=None,
    platforms="facebook,instagram",
    lang=None,
):
    """
    Retrieve posts from Facebook/Instagram based on the passed parameters.
    REF: https://github.com/CrowdTangle/API/wiki/Search
    Parameters:
        - count (int, optional): The number of posts to return.
            Options: [1-100]
            Default: 10
        - start_time (str, datetime_obj, optional): The earliest time at which a post could be posted.
            Time zone is UTC.
            String format: “yyyy-mm-ddThh:mm:ss” or “yyyy-mm-dd”
                - If date with no time is passed, default time granularity = 00:00:00
        - end_time (str, datetime_obj, optional): The latest time at which a post could be posted.
            Time zone is UTC.
            String format: “yyyy-mm-ddThh:mm:ss” or “yyyy-mm-dd”
                - If date with no time is passed, default time granularity = 00:00:00
            Default time: "now"
        - include_history (str, optional): Includes time step data for the growth of each post returned.
            Options: 'true'
            Default: null (not included)
        - sort_by (str, optional): The method by which to filter and order posts.
            Options:
                - 'date'
                - 'interaction_rate'
                - 'overperforming'
                - 'total_interactions'
                - 'underperforming'
            Default: 'overperforming'
        - types (str, optional): The types of post to include. These can be separated by commas to
            include multiple types. If you want all live videos (whether currently or formerly live),
            be sure to include both live_video and live_video_complete. The "video" type does not
            mean all videos, it refers to videos that aren't native_video, youtube or vine (e.g. a
            video on Vimeo).
            Options:
                - "episode"
                - "extra_clip"
                - "link"
                - "live_video"
                - "live_video_complete"
                - "live_video_scheduled"
                - "native_video"
                - "photo"
                - "status"
                - "trailer"
                - "video"
                - "vine"
                -  "youtube"
            Default: all
        - search_term (str, optional): Returns only posts that match this search term.
            Terms AND automatically. Separate with commas for OR, use quotes for phrases.
            E.g. CrowdTangle API -> AND. CrowdTangle, API -> OR. "CrowdTangle API" -> AND in that
            exact order. You can also use traditional Boolean search with this parameter.
            Default: null
        - account_types: Limits search to a specific Facebook account type. You can use more than
            one type. Requires "platforms=facebook" to be set also. If "platforms=facebook" is not
            set, all post types including IG will be returned. Only applies to Facebook.
            Options:
                - facebook_page
                - facebook_group
                - facebook_profile
            Default: None (no restrictions, all platforms)
        - min_interactions (int, optional): If set, will exclude posts with total interactions
            below this threshold.
            Options: int >= 0
            Default: 0
        - offset (int, optional): The number of posts to offset (generally used for pagination).
            Pagination links will also be provided in the response.
        - api_token (str, optional): The API token needed to pull data. You can locate your API
            token via your CrowdTangle dashboard under Settings > API Access.
        - platforms: the platform to collect data from
            Options: "facebook", "instagram", or "facebook,instagram" (both)
            Default: "facebook,instagram"
        - lang: language of the posts to collect (str)
            Default: None (no restrictions)
            Options: 2-letter code found in reference below. See ref above for some exceptions.
            REF:https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    Returns:
        [dict]: The Response contains both a status code and a result. The status will always
            be 200 if there is no error. The result contains an array of post objects and a
            pagination object with URLs for both the next and previous page, if they exist
    Example:
        ct_get_posts(include_history = 'true', api_token="AKJHXDFYTGEBKRJ6535")
    """

    # API-endpoint
    URL_BASE = "https://api.crowdtangle.com/posts/search"
    # Defining a params dict for the parameters to be sent to the API
    PARAMS = {
        "count": count,
        "sortBy": sort_by,
        "token": api_token,
        "minInteractions": min_interactions,
        "offset": offset,
    }

    # add params parameters
    if start_time:
        PARAMS["startDate"] = start_time
    if end_time:
        PARAMS["endDate"] = end_time
    if include_history == "true":
        PARAMS["includeHistory"] = include_history
    if types:
        PARAMS["types"] = types
    if account_types:
        PARAMS["accountTypes"] = account_types
    if search_term:
        PARAMS["searchTerm"] = search_term
    if platforms:
        PARAMS["platforms"] = platforms
    if lang:
        PARAMS["language"] = lang

    # sending get request and saving the response as response object
    r = requests.get(url=URL_BASE, params=PARAMS)
    if r.status_code != 200:
        print(f"status: {r.status_code}")
        print(f"reason: {r.reason}")
        print(f"details: {r.raise_for_status()}")
    return r


if __name__ == "__main__":
    args = parse_cl_args_ct_dl()
    domains_filepath = args.domains_file  # Includes one domain on each line
    output_dir = args.out_dir

    print(f"Domains file: {domains_filepath}")

    # Load domains to match in below query and clean up
    domains = load_lines(domains_filepath)
    domains = [domain.lstrip("https://") for domain in domains]
    domains = [domain.lstrip("www.") for domain in domains]
    domains = [domain.rstrip("/*") for domain in domains]

    # Load CrowdTangle token
    ct_token = os.environ.get("TOP_FIBERS_TOKEN")
    if ct_token is None:
        raise ValueError(
            "Crowdtangle API token not set as an environment variable. "
            "Run: <export TOP_FIBERS_TOKEN='INSERT_TOKEN_HERE'> and try again."
        )

    # Set start and end dates
    if OFFSET > 0:
        raise ValueError("OFFSET must be <= 0.")
    start_date, end_date = get_start_and_end_dates(
        num_months=NUMBER_OF_MONTHS_TO_PULL, offset=OFFSET
    )

    print(f"Start date  : {start_date}")
    print(f"End date    : {end_date}")

    # Create output filename with time period
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    output_file_path = os.path.join(
        output_dir, f"{start_str}--{end_str}__fb_posts_w_links.jsonl.gzip"
    )

    print(f"Output file : {output_file_path}")

    # Open file here so we don't have to hold data in memory
    with gzip.open(output_file_path, "wb") as f:

        # Iterate through each site
        for idx, domain in enumerate(domains, start=1):
            print(f"Collect posts matching domain {idx} of {len(domains)}: {domain}")

            total_posts = 0
            query_count = 0
            try_count = 0
            max_attempts = 7

            first_call = True
            more_data = False
            while first_call or more_data:
                try:
                    if first_call:
                        time.sleep(WAIT_BTWN_POSTS)
                        response = ct_get_search_posts(
                            count=NUMBER_OF_POSTS_PER_CALL,
                            start_time=start_date,
                            end_time=end_date,
                            include_history=None,
                            sort_by="date",
                            types=None,
                            search_term=domain,
                            account_types=None,
                            min_interactions=0,
                            offset=0,
                            api_token=ct_token,
                            platforms="facebook",
                            lang=None,
                        )

                    else:
                        # This is the full URL returned by CT to continue pulling data
                        # from the next page. See block below.
                        time.sleep(WAIT_BTWN_POSTS)
                        response = requests.get(next_page_url)

                    response_json = response.json()

                    # Returns a list of dictionaries where each dict represents one post.
                    posts = response_json["result"]["posts"]
                    num_posts = len(posts)

                    # Flip first_call if we get a successful first call with posts
                    # NOTE: repeated first calls with no data will break after too many attempts
                    if first_call:
                        if (response_json["status"] == 200) and (num_posts != 0):
                            print("Successful first call.")
                            print("Setting first_call = False")
                            first_call = False

                    # Reset and then grab the pagination url if it is there
                    next_page_url = None
                    if "pagination" in response_json["result"]:
                        if "nextPage" in response_json["result"]["pagination"]:
                            next_page_url = response_json["result"]["pagination"][
                                "nextPage"
                            ]
                            print(f"Found next page: {next_page_url}")
                            more_data = True

                    if next_page_url is None:
                        more_data = False

                except Exception as e:  # 2 calls/minute limit if you request them
                    print(e)
                    try:
                        print(f"FB message: {response_json['message']}")
                    except:
                        pass

                    # Handle the retries...
                    try_count += 1
                    print(f"There are {max_attempts-try_count} tries left.")
                    if (max_attempts - try_count) <= 0:
                        print("Breaking out of loop!")
                        break
                    else:
                        wait_time = WAIT_BTWN_ERROR_BASE**try_count
                        if wait_time > 60:
                            wait_time = wait_time / 60
                            print(f"Waiting {wait_time} minutes...")
                        else:
                            print(f"Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        print(f"Retrying...")
                        continue

                else:
                    if num_posts == 0:
                        print("Zero posts were returned.")
                        try_count += 1
                        print(f"There are {max_attempts-try_count} retries left.")

                        if (max_attempts - try_count) <= 0:
                            print("Breaking out of loop!")
                            break
                        else:
                            wait_time = WAIT_BTWN_ERROR_BASE**try_count
                            if wait_time > 60:
                                wait_time = wait_time / 60
                                print(f"Waiting {wait_time} minutes...")
                            else:
                                print(f"Waiting {wait_time} seconds...")
                            time.sleep(wait_time)
                            print(f"Retrying...")
                            continue

                    else:
                        # Reset the try count to zero
                        try_count = 0

                        most_recent_date_str = posts[0]["date"]
                        oldest_date_str = posts[-1]["date"]
                        print(
                            f"\t|--> {oldest_date_str} - {most_recent_date_str}"
                            f": {num_posts:,} posts."
                        )

                        # Convert each post into bytes with a new-line (`\n`)
                        for post in posts:
                            post_in_bytes = f"{json.dumps(post)}\n".encode(
                                encoding="utf-8"
                            )
                            f.write(post_in_bytes)

                        total_posts += num_posts
                        print(f"Total posts collected: {total_posts:,}")

                    # More than 5_000 queries (~5M posts), we break the script.
                    query_count += 1
                    if query_count > 5_000:
                        break
