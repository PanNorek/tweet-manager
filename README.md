# tweet-manager
A simple app for collecting tweets from Twitter API by given hashtags or account name

# 📂 Directory Structure
    ├───assets
    └───data
        ├───notepad2
        ├───src
        │   └───tweetscrapper
        └───tests
       

# 🚀 How to run
## Project Setup

<li>Create a virtual environment using <code> virtualenv venv </code>
<li>Activate the virtual environment by running <code> venv/bin/activate </code>
<li>On Windows use <code> venv\Scripts\activate.bat </code>
<li>Install the dependencies using <code> pip install -r requirements.txt </code>
<li>Open Edit Configuration File to configure your setup.
<li>Edit Run.bat file to specify your python path.
<li>Double click Run.bat file and enjoy!

<li>You can check unittests by switching folder from root to data and typing <code>python -m unittest </code>

## Twitter developer account
1. Login to your account on Twitter <a>https://twitter.com/login</a>
2. Create dev account <a>https://developer.twitter.com/en/portal/petition/essential/basic-info</a>
3. Create a new app and project.  <a>https://developer.twitter.com/en/portal/dashboard</a>
4. Copy all the keys from the app and keep them in the <code>api_keys.json</code> file (this version only needs the bearer token)
You can paste your keys in the <code>your_api_keys_sample.json</code> file and cut off 'your_' and '_sample' from the file name.

## Configuration file – basic informations
This section contains minimum information that you need to know to quickly run tweet-manager.

Follow these steps to run your first job with tweet-manager:

1. Open configuration file (you can simply open it by clicking Edit Configuration File.bat
2. Specify keys_path as a full (absolute) path to the json file where your Twitter Api keys are stored.

3. Run tweet-manager.

This will create output file with a name specified by output_path in the input folder (location of input file).

## Configuration file – details and advanced features
A job is defined by 5 parameters:
<li> keys_path - absolute (full) path to the json file where your Twitter Api keys are stored.
<li> max_results - number of tweets taken by specified hashtag/user
<li> all_conversation - True/False if you what the tweets with replies(default number of replies per tweet is 100)
<li> output_path - path to the output file. It can be absolute or relative to the folder where the input file is located. It may contain tags <date>, <mode> and <max_results> that are replaced with proper values at runtime.
And one of these two:
<li> hashtag - name of desired hashtag
<li> account_name - name of account

## Example configuration files
1. Single mode
![Screenshot](/assets/config_single.png)

2. Batch mode
![Screenshot](/assets/config.png)
  As you can see - the vast part of parameters can be stored in [DEFAULT] section of config file. The only one thing you have to specify in the jobs is the hashtag or account name.

# 📅 Development Schedule
## Version 1.0.0
- [x] Beta version (Minimum viable product)

## Version 1.1.0
- [x] Merge all json files into big one
- [ ] Add tool to find current most popular hashtags

# 📧 Contact
  If you find a bug, you have an idea for improvement or you need help, let me know:
[![](https://img.shields.io/twitter/url?label=/rafal-nojek/&logo=linkedin&logoColor=%230077B5&style=social&url=https%3A%2F%2Fwww.linkedin.com%2in%2rafaln97%2F)](https://www.linkedin.com/in/rafaln97/) [![](https://img.shields.io/twitter/url?label=/PanNorek&logo=github&logoColor=%23292929&style=social&url=https%3A%2F%2Fgithub.com%2FPanNorek)](https://github.com/PanNorek)
