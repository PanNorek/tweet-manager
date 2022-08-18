import datetime
import io
from src.tweetscrapper.AuthorizationManager import AuthorizationManager
from src.tweetscrapper.TweetManagers import *
import os
import sys
import getopt
import configparser
import time
import json


def main():
    """Main program"""
    settings_path = "settings.ini"
    OUTPUT_PATH = "outputs"
    OUTPUT_FILENAME = f"{datetime.datetime.now().strftime('%m-%d-%Y')}-merged.json"

    app_settings = settings_read(settings_path)

    splash_screen()

    # Get config path from arguments
    all_args = sys.argv[1:]
    try:
        opts, arg = getopt.getopt(all_args, "c:")
    except getopt.GetoptError:
        opts = []

    arg_config_path = ""
    for o in opts:
        if o[0] == "-c":
            arg_config_path = o[1]

    if arg_config_path == "":
        info("Configuration file not specified - I cannot continue :(\n")
        info("usage: main.py -c <config_path>\n(eg. main.py -c config.ini)")
        wait_for_enter("\nPress Enter to exit.")
        app_exit()

    # Read and prepare config
    info(f"Configuration file: {arg_config_path}")
    try:
        configs_raw = config_read(config_path=arg_config_path)

        configs = config_add_dtypes(configs_raw)
        num_configs = len(configs)
        info(f"Number of configurations/jobs: {num_configs} ", end="")

    except Exception as e:
        info(f"ERROR: {e}")
        wait_for_enter("\nPress Enter to exit")
        app_exit()

    # Check config
    # problem_idx = config_sanity_check(configs)
    # TODO: write sanity check function

    problem_idx = -1
    if problem_idx > -1:
        info("\n\nInvalid configuration detected:")
        show_config(configs[problem_idx])
        wait_for_enter("\nFix the problem and restart.\nPress Enter to exit.")
        app_exit()

    # Activate single-file or batch mode
    if num_configs == 0:
        # 0 configs - Should never reach this point.
        #  This should have been handled in sanity check.
        info("(No config, no job)")

    elif num_configs == 1:
        # 1 config - Single file mode - detailed info
        config = configs[0]
        info("(Single file mode)")
        info("\nConfiguration:")
        show_config(config)
        info("")
        # notTODO: _______(Optional) Display WARNING if output file exists
        wait_for_enter("Press Enter to continue (or close the window to exit)")
        tweet_manager_core(config, app_settings, verbose=True, overwrite=True)

    else:
        # 2 and more configs - Batch mode
        info("(Batch mode)")
        est_time = num_configs * app_settings["job_exec_time"]
        info(f"\nEstimated total time: {est_time:.0f} seconds")
        info("")
        # notTODO: Display WARNING if output files exist
        wait_for_enter("Press Enter to continue (or close the window to abort)")
        progress_bar(0, num_configs)
        # stats = {'ok': 0, 'error': 0, 'skipped': 0}
        # TODO: add statistics
        tic = time.time()
        for i, config in enumerate(configs):
            tweet_manager_core(config, app_settings, verbose=True, overwrite=True)
            time.sleep(15)  # wait so as not to reach api download limits
            progress_bar(
                i + 1,
                num_configs,
                msg=f"{config['account_name'] if 'account_name' in config.keys() else config['hashtag']},"
                f" {'with_replies' if config['all_conversation'] else 'no_replies'} ",
            )  # TODO: -> {result}

        merge_jsons(OUTPUT_PATH, OUTPUT_FILENAME)

        toc = time.time()
        total_time = toc - tic
        progress_bar(num_configs, num_configs, msg=f"Done ({total_time:.1f} seconds)")
        info("")


def settings_read(config_path):
    """
    Read application settings from INI file

    """
    num_params = ["job_exec_time"]
    app_settings = config_read(config_path, num_params=num_params)
    app_settings = app_settings[0]

    return app_settings


def progress_bar(i, total, msg=""):

    bar_width = 80

    # Prepare new bar's content
    # 1. Progress info
    head = f"{i/total:>4.0%} ({i}/{total})"
    # 2. Message
    tail = msg

    #      msg = 'Hello little flower...'
    # long msg = 'Hello little flower, its very nice to meet you, bla, blabla, bla, blabla, bla, bla.. This is the end'

    # pad or crop tail, to get head+tail with length=bar_width
    hlen = len(head)
    tlen = bar_width - hlen - 1  # -1 because of space separating head and tail
    # msglen = len(msg)

    tail = tail.ljust(tlen, " ")  # pad
    tail = tail[:tlen]  # crop

    pbar = head + " " + tail  # 'pbar' because 'bar' is blacklisted in pylint

    if len(pbar) == bar_width:
        pass  # ok
    else:
        print("\n\nbar length", len(pbar))
        raise Exception("WTF bar?")

    # Return the carriage and print new
    print(f"\r{pbar}", end="", flush=True)


def config_read(config_path="config.ini", num_params=[]):
    """
    Read job configuration from INI file

    """

    config_path = os.path.join(os.getcwd(), "data", config_path)

    if os.path.exists(config_path):
        config_parser = configparser.ConfigParser()
        config_parser.read(config_path)
        config_sections = config_parser.sections()
        config_raw = []
        for s in config_sections:
            # print(dict(config_parser[s]))
            config_raw.append(dict(config_parser[s]))

        # Convert numeric params
        for item in config_raw:
            for p in num_params:
                item[p] = float(item[p])

        return config_raw

    else:
        raise Exception(f"Config file '{config_path}' does not exist")


def splash_screen():
    """
    Show splash screen along with a version number.

    """
    ver = version()
    S = f"""
                            Welcome to the Tweet Manager!
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@((((((((((((((@@@@@@@((@@
            @@@@(((@@@@@@@@@@@@@@@@@@@@@@@@@(((((((((((((((((((((((((@@@
            @@@(((((((@@@@@@@@@@@@@@@@@@@@@(((((((((((((((((((((((@&(((@
            @@@((((((((((@@@@@@@@@@@@@@@@@(((((((((((((((((((((((((((@@@
            @@@@((((((((((((((@@@@@@@@@@@@((((((((((((((((((((((((@@@@@@
            @@@@@(((((((((((((((((((((((@@((((((((((((((((((((((((@@@@@@
            @@@(@@@(((((((((((((((((((((((((((((((((((((((((((((((@@@@@@
            @@@(((((((((((((((((((((((((((((((((((((((((((((((((((@@@@@@
            @@@@(((((((((((((((((((((((((((((((((((((((((((((((((@@@@@@@
            @@@@@@((((((((((((((((((((((((((((((((((((((((((((((@@@@@@@@
            @@@@@@@@@((((((((((((((((((((((((((((((((((((((((((@@@@@@@@@
            @@@@@@@@((((((((((((((((((((((((((((((((((((((((((@@@@@@@@@@
            @@@@@@@@@((((((((((((((((((((((((((((((((((((((((@@@@@@@@@@@
            @@@@@@@@@@@((((((((((((((((((((((((((((((((((((@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@((((((((((((((((((((((((((((@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@(((((((((((((((((((((((((((@@@@@@@@@@@@@@@@@@
            @@@@@@@@(((((((((((((((((((((((((((((((@@@@@@@@@@@@@@@@@@@@@
            @@@@@(((((((((((((((((((((((((((((@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@((((((((((((((@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                              ver. {ver}
                              """
    print(S)


def version():
    """Application version"""
    return "1.0.0 (beta)"  # (Major.Minor.Bugfix, update when needed)


def info(*args, **kwargs):
    """
    Display info (like print function do).

    """

    print(*args, **kwargs)


def cinfo(flag, *args, **kwargs):
    """
    Display info only if flag is True

    Just a wrapper for info().
    """

    if flag:
        info(*args, **kwargs)


def wait_for_enter(prompt="Press Enter to continue..."):
    """
    Wait for (input and) pressing Enter

    """
    info(prompt)
    return input()


def app_exit():
    """
    Exit the application and close the window

    """
    sys.exit(0)


def config_add_dtypes(config_raw):
    """
    Convert config items to proper data types (for later convenience).

    """

    num_params = ["max_results"]
    bool_params = ["all_conversation"]
    # Convert numeric params
    for item in config_raw:
        for p in num_params:
            item[p] = int(item[p])

    for item in config_raw:
        for p in bool_params:
            item[p] = eval(item[p])
    return config_raw


def show_config(config):
    """
    Pretty-print configuration dictionary

    """
    for k in config.keys():
        info(f"    {k} = {config[k]}")


def output_prepare_path(config, start_dir):
    """
    Prepare absolute output path (config['output_path'] may be absolute or relative)

    If config['output_path'] is absolute just return it.
    If it is relative, calculate it's absolute form using start_dir as a start.
    """
    if "hashtag" in config.keys():
        tag_dict = {
            "<date>": datetime.datetime.now().strftime("%m-%d-%Y"),
            "<mode>": config["hashtag"],
            "<max_results>": str(config["max_results"]),
        }
    elif "account_name" in config.keys():
        tag_dict = {
            "<date>": datetime.datetime.now().strftime("%m-%d-%Y"),
            "<mode>": config["account_name"],
            "<max_results>": str(config["max_results"]),
        }

    cfg_output_path = config["output_path"]

    # Replace tags with respective values
    for tag in tag_dict:
        cfg_output_path = cfg_output_path.replace(tag, str(tag_dict[tag]))

    # Convert to absolute
    if os.path.isabs(cfg_output_path):
        return cfg_output_path
    else:
        in2out = os.path.join(start_dir, cfg_output_path)
        cwd2out = os.path.relpath(in2out, start=os.curdir)
        absout = os.path.abspath(cwd2out)
        return absout


def merge_json_files(output_path: str, output_filename: str):
    """Compress many json files into bigger one

    Args:
        output_path (str):  it is what it is
        output_filename (str): it also
    """
    output_dir = os.path.join(os.getcwd(), output_path)
    result = list()
    for dirname, _, filenames in os.walk(output_dir):
        for filename in filenames:
            with open(os.path.join(dirname, filename), "r", encoding="utf-8") as infile:
                result.extend(json.load(infile))

    with open(
        os.path.join(output_dir, output_filename), "w", encoding="utf-8"
    ) as output_file:
        json.dump(result, output_file)


def tweet_manager_core(config, app_settings, verbose, overwrite):
    """
    Do the job defined by the config.

    If verbose is True informations about the progress will be printed.

    Return a message describing the result of a job execution:
        'ok'           - if everything is ok
        'error'        - if error happened
        'error:abc...' - the same as above but with a more detailed error information ('abc...')
    """

    # ============== 1. Read Tweeter API keys ==============
    tic = time.time()
    auth = AuthorizationManager(config["keys_path"]).get_bearer_token()
    toc = time.time()
    cinfo(verbose, "OK (%.3f seconds)" % (toc - tic))
    # ============== 2. Do processing ==============
    cinfo(verbose, "Processing... ", end="")

    tic = time.time()
    if "hashtag" in config.keys():
        data, _ = get_json_tweets_by_hashtag(
            auth, config["hashtag"], config["max_results"], app_settings["lang"]
        )
    elif "account_name" in config.keys():
        data, _ = get_tweets_by_acc_name(
            auth, config["account_name"], config["max_results"], app_settings["lang"]
        )
    else:
        # Program can only get tweet by either hashtag or account name
        raise Exception

    if config["all_conversation"]:
        all_replies = []
        conversation_ids = get_conversation_ids(data)
        if conversation_ids is not None:
            for conversation_id in conversation_ids:
                replies, _ = get_replies(
                    auth,
                    conversation_id,
                    app_settings["reply_count"],
                    app_settings["lang"],
                )
                all_replies.append(replies)

    if data is not None:
        data.append(all_replies)

        toc = time.time()
        cinfo(verbose, "OK (%.3f seconds)" % (toc - tic))
        # ============== 3. Write outputs ==============
        cinfo(verbose, "Writing output... ", end="", flush=True)
        tic = time.time()
        start_dir = os.path.split(config["keys_path"])[0]
        output_path = output_prepare_path(config, start_dir)

        with io.open(output_path, "w", encoding="utf8") as outfile:
            str_ = json.dumps(
                data,
                indent=4,
                sort_keys=True,
                separators=(",", ": "),
                ensure_ascii=False,
            )
            outfile.write((str_))
        toc = time.time()
        cinfo(verbose, "OK (%.3f seconds)" % (toc - tic))


if __name__ == "__main__":
    main()
