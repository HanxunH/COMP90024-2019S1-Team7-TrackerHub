# @Author: Hanxun Huang <hanxunhuang>
# @Date:   2019-05-05T14:10:41+10:00
# @Email:  hanxunh@student.unimelb.edu.au
# @Filename: coconut_image_recong.py
# @Last modified by:   hanxunhuang
# @Last modified time: 2019-05-05T19:44:00+10:00
import argparse
import logging
import io
import operator
import os
import requests
import json
import time
from PIL import Image
from coconut_inference import coconut_inference

API_KEY = '227415ba68c811e9b1a48c8590c7151e'
parser = argparse.ArgumentParser(description='COMP90024 Project Coconut Image Recongnation')

parser.add_argument('--load_with_config', action='store_true')
parser.add_argument('--config_file_path', type=str, default='config/config.json')

parser.add_argument('--server_address', type=str, default='172.26.38.1')
parser.add_argument('--server_port', type=int, default=8080)
parser.add_argument('--trained_tweet_api', type=str, default='/api/tweet/trained/')
parser.add_argument('--untrained_tweet_api', type=str, default='/api/tweet/untrained/')
parser.add_argument('--pic_tweet_api', type=str, default='/api/tweet/pic/')
parser.add_argument('--log_file_path', type=str, default='logs/coconut_image_recong.log')
parser.add_argument('--food179_checkpoints', type=str, default='checkpoints/food179_resnet101_sgd.pth_best.pth')
parser.add_argument('--nsfw_checkpoints', type=str, default='checkpoints/nsfw_resnet101_sgd_v3.pth_best.pth')
parser.add_argument('--server_rest_time', type=int, default=30, help='Sleep for X minuts if no new data ready')
parser.add_argument('--batch_size', type=int, default=100)

args = parser.parse_args()


class coconut_image_recong:
    def load_config_with_args(self):
        self.server_address = args.server_address
        self.server_port = args.server_port
        self.trained_tweet_api = args.trained_tweet_api
        self.untrained_tweet_api = args.untrained_tweet_api
        self.pic_tweet_api = args.pic_tweet_api
        self.log_file_path = args.log_file_path
        self.food179_checkpoints = args.food179_checkpoints
        self.nsfw_checkpoints = args.nsfw_checkpoints
        self.server_rest_time = args.server_rest_time
        self.batch_size = args.batch_size
        return

    def load_config_with_file(self, file_path):
        with open(file_path) as json_file:
            config = json.load(json_file)
            self.server_address = config['server_address']
            self.server_port = config['server_port']
            self.trained_tweet_api = config['trained_tweet_api']
            self.untrained_tweet_api = config['untrained_tweet_api']
            self.pic_tweet_api = config['pic_tweet_api']
            self.log_file_path = config['log_file_path']
            self.food179_checkpoints = config['food179_checkpoints']
            self.nsfw_checkpoints = config['nsfw_checkpoints']
            self.server_rest_time = config['server_rest_time']
            self.batch_size = config['batch_size']
        return

    def __init__(self):
        super()

        # Parse Argument
        if args.load_with_config:
            self.load_config_with_file(args.config_file_path)
        else:
            self.load_config_with_args()

        self.request_server_url = 'http://' + self.server_address + ':' + str(self.server_port)
        self.set_logger()

        # Inference Setup
        self.nsfw_version = os.path.splitext(os.path.basename(self.nsfw_checkpoints))[0]
        self.nsfw_model = coconut_inference(model_checkpoint_file_path=self.nsfw_checkpoints)
        self.logger.info('NSFW Model Version: %s' % (self.nsfw_version))
        self.logger.info('\n%s' % (self.nsfw_model.print_model_details()))

        self.food179_version = os.path.splitext(os.path.basename(self.food179_checkpoints))[0]
        self.food179_model = coconut_inference(model_checkpoint_file_path=self.food179_checkpoints)
        self.logger.info('Food179 Model Version: %s' % (self.food179_version))
        self.logger.info('\n%s' % (self.food179_model.print_model_details()))

        self.logger.info('Coconut Image Recongnation Initialized')
        return

    def set_logger(self):
        logger_level = logging.INFO
        self.logger = logging.getLogger('Main')
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s - %(funcName)s(): %(message)s')

        # create file handler which logs even debug messages
        fh = logging.FileHandler(self.log_file_path)
        fh.setLevel(logger_level)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logger_level)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.setLevel(logger_level)

    def test_connection(self):
        response = os.system("ping -c 1 " + self.server_address)
        if response == 0:
            self.logger.info('Sever Address: %s is up' % (self.server_address))
            return True
        else:
            self.logger.error('Sever Address: %s is Down' % (self.server_address))
            return False


    def api_get(self, request_url):
        headers = {'X-API-KEY' : API_KEY}
        try:
            response = requests.get(request_url, headers=headers)
            if response.status_code != requests.codes.ok:
                self.logger.error(response.status_code)
                self.logger.error(response.content)
                return
            return response
        except Exception as error:
            self.logger.error(error)
        return

    def api_post(self, request_url, payload):
        headers = {'X-API-KEY' : API_KEY}
        try:
            response = requests.post(request_url, headers=headers, json=payload)
            if response.status_code != requests.codes.ok:
                self.logger.error(response.status_code)
                self.logger.error(response.content)
                return
            return response
        except Exception as error:
            self.logger.error(error)
        return

    # Request tweets data from Server
    def request_tweets(self):
        request_url = self.request_server_url + self.untrained_tweet_api + str(self.batch_size) + '/'
        response = self.api_get(request_url)
        if response is not None:
            try:
                return json.loads(response.content)
            except Exception as error:
                self.logger.error(error)
        return None

    # Request single image by img_id
    def request_image(self, img_id):
        request_url = self.request_server_url + self.pic_tweet_api + img_id + '/'
        response = self.api_get(request_url)
        if response is not None:
            try:
                image = Image.open(io.BytesIO(response.content))
                return image
            except Exception as error:
                self.logger.error(error)
        return None

    # Helper Function process list of result to dictionary
    def process_list_rs_to_dict(self, list_rs):
        rs_dict = {}
        for item in list_rs:
            rs_dict[item[0]] = item[1]
        return rs_dict

    # Process single tweet
    def process_single_tweet(self, tweet_data_id, json_data):
        tweet_data_img_ids = json_data['img_id']
        tweet_data_tags = json_data['tags']
        tweet_data_model = json_data['model']
        food179_rs_list = []
        nsfw_rs_list = []
        # Some tweet have more than 1 image
        for img_id in tweet_data_img_ids:
            img = self.request_image(img_id)
            if img is None:
                continue
            try:
                start = time.time()
                food179_rs = self.food179_model.inference(image_path=img, num_of_perdict=5, is_img_data=True)
                nsfw_rs = self.nsfw_model.inference(image_path=img, num_of_perdict=5, is_img_data=True)
                food179_rs_list.append(food179_rs)
                nsfw_rs_list.append(nsfw_rs)

                end = time.time()
                self.logger.debug('inference %.4fs' % (end - start))
                self.logger.debug(food179_rs)
                self.logger.debug(nsfw_rs)
            except Exception as error:
                self.logger.error('tweet_id: %s, img_id: %s, error: %s' % (tweet_data_id, tweet_data_img_ids, error))

        # Handle tweeet have more than 1 image
        if len(nsfw_rs_list) > 0:
            nsfw_rs = nsfw_rs_list[0]
            food179_rs = food179_rs_list[0]
            for index in range(len(food179_rs_list)):
                target_nsfw_rs = nsfw_rs_list[index]
                target_food179_rs = food179_rs_list[index]
                if target_nsfw_rs[0][1] > nsfw_rs[0][1]:
                    nsfw_rs = target_nsfw_rs
                if target_food179_rs[0][1] > food179_rs[0][1]:
                    food179_rs = target_food179_rs

            nsfw_rs_dict = self.process_list_rs_to_dict(nsfw_rs)
            food179_rs_dict = self.process_list_rs_to_dict(food179_rs)
            result_payload = {
                'tags':{
                    'nsfw' : nsfw_rs_dict,
                    'food179': food179_rs_dict
                },
                'model':{
                    'nsfw' : self.nsfw_version,
                    'food179' : self.food179_version
                }
            }
            return result_payload
        return

    # Process Tweets data
    def process_tweets_json(self, json_data):
        if json_data is None:
            self.logger.error('Response json_data is None')
            return
        if 'data' not in json_data:
            self.logger.error('Key: data not in request_tweets() response')
            return
        data_json = json_data['data']
        if len(data_json) == 0:
            return False
        result_payload = {}
        for tweet_data_id in data_json:
            rs_dict = self.process_single_tweet(tweet_data_id, data_json[tweet_data_id])
            if rs_dict is not None:
                result_payload[tweet_data_id] = rs_dict
        self.upload_result(result_payload)
        return True

    # Upload Results
    def upload_result(self, payload):
        request_url = self.request_server_url + self.trained_tweet_api
        response = self.api_post(request_url, payload)
        if response:
            response = json.loads(response.content)
            self.logger.debug(response)
            if 'data' in response and len(response['data']) > 0 :
                self.logger.info('Uploaded %d tweets result' % (len(response['data'])))
            else:
                self.logger.error('Someting went wrong with upload result')
        else:
            self.logger.error('Someting went wrong with upload result')
        return

    def main(self):
        while True:
            self.logger.info('Requesting tweets, batch_size %d' % (self.batch_size))
            target_tweets_json = self.request_tweets()
            self.logger.debug(target_tweets_json)
            if target_tweets_json is not None:
                response = self.process_tweets_json(target_tweets_json)
                if response is not None and not response:
                    self.logger.info('No Data Available, Sleep for %d minute' % (self.server_rest_time))
                    time.sleep(self.server_rest_time*60)
            # Avoid too much request Sleep for 30 second
            self.logger.info('Avoid too much request Sleep for 10 Second')
            time.sleep(10)
        return

if __name__ == "__main__":
    ops = coconut_image_recong()
    ops.main()
