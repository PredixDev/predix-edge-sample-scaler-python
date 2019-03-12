import unittest
import src.app


class TestApp(unittest.TestCase):

    def setUp(self):
        '''Simulated OPC-UA data'''
        self.from_broker_one_tag = {"messageId": "flex-pipe", "body": [{"attributes":{"machine_type": "opcua"}, "datapoints": [[1537377630622, 80.0, 3]], "name": "My.App.DOUBLE1"}]}
        self.from_broker_two_different_tags = {"messageId": "flex-pipe", "body": [{"attributes":{"machine_type": "opcua"}, "datapoints": [[1537377630622, 80.0, 3]], "name": "My.App.DOUBLE1"}, {"attributes":{"machine_type": "opcua"}, "datapoints": [[1537377630622, 112.64, 3]], "name": "My.App.DOUBLE2"}]}
        self.from_broker_two_same_tags = {"messageId": "flex-pipe", "body": [{"attributes":{"machine_type": "opcua"}, "datapoints": [[1537377630622, 80.0, 3]], "name": "My.App.DOUBLE1"}, {"attributes":{"machine_type": "opcua"}, "datapoints": [[1537377630622, 112.64, 3]], "name": "My.App.DOUBLE1"}]}

    def test_one_tag_no_match(self):
        '''Test the scaling function with one tag that does not match - no change expected'''
        one_tag_no_change = {"messageId": "flex-pipe", "body": [{"attributes":{"machine_type": "opcua"}, "datapoints": [[1537377630622, 80.0, 3]], "name": "My.App.DOUBLE1"}]}
        self.assertEqual(src.app.scale_data(self.from_broker_one_tag, "My.App.DOUBLE2"), one_tag_no_change)

    def test_one_tag_yes_match(self):
        '''Test the scaling function with one tag that does match - change expected'''
        one_tag_yes_change = {"messageId": "flex-pipe", "body": [{"attributes":{"machine_type": "opcua"}, "datapoints": [[1537377630622, 80000, 3]], "name": "My.App.DOUBLE1.scaled_x_1000"}]}
        self.assertEqual(src.app.scale_data(self.from_broker_one_tag, "My.App.DOUBLE1"), one_tag_yes_change)

    def test_two_tags_no_match(self):
        '''Test the scaling function with two tags that do not match - no change expected'''
        two_tags_no_change = {"messageId": "flex-pipe", "body": [{"attributes":{"machine_type": "opcua"}, "datapoints": [[1537377630622, 80.0, 3]], "name": "My.App.DOUBLE1"}, {"attributes":{"machine_type": "opcua"}, "datapoints": [[1537377630622, 112.64, 3]], "name": "My.App.DOUBLE2"}]}
        self.assertEqual(src.app.scale_data(self.from_broker_two_different_tags, "My.App.DOUBLE3"), two_tags_no_change)
    
    def test_two_tags_one_match(self):
        '''Test the scaling function with two tags, one of which matches - one change expected'''
        two_tags_one_change = {"messageId": "flex-pipe", "body": [{"attributes":{"machine_type": "opcua"}, "datapoints": [[1537377630622, 80.0, 3]], "name": "My.App.DOUBLE1"}, {"attributes":{"machine_type": "opcua"}, "datapoints": [[1537377630622, 112640, 3]], "name": "My.App.DOUBLE2.scaled_x_1000"}]}
        self.assertEqual(src.app.scale_data(self.from_broker_two_different_tags, "My.App.DOUBLE2"), two_tags_one_change)

    def test_two_tags_both_match(self):
        '''Test the scaling function with two tags that match - change expected'''
        two_tags_both_change = {"messageId": "flex-pipe", "body": [{"attributes":{"machine_type": "opcua"}, "datapoints": [[1537377630622, 80000, 3]], "name": "My.App.DOUBLE1.scaled_x_1000"}, {"attributes":{"machine_type": "opcua"}, "datapoints": [[1537377630622, 112640, 3]], "name": "My.App.DOUBLE1.scaled_x_1000"}]}
        self.assertEqual(src.app.scale_data(self.from_broker_two_same_tags, "My.App.DOUBLE1"), two_tags_both_change)

    
