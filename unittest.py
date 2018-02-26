import unittest
from publisher import * 
from subscriber import *
from proxy import *

def assert_false(x):
    if bool(x) is False:
        return True   
    else:
        return False

def assert_true(x):
    if bool(x) is True:
        return True   
    else:
        return False

def assert_equal(a, b):
    if a == b:
        return True
    else:
        return False

class Test():
    """Test the API between the proxy and publisher/subscriber"""
    #def __init__(self,*args, **kwargs):
    #def setUp(self):
    def __init__(self):
        self.test_proxy = Proxy()
        self.test_pub = Publisher("127.0.0.1",4)
        self.test_sub = Subscriber("127.0.0.1","5556","10001")

    def test_proxy_publisher(self):
        """Test sockets of proxy-publisher"""
        print "#############################################"
        print "Test sockets of proxy-publisher"
        #print assert_false(self.test_proxy.xsubsocket.closed)
        #print assert_false(self.test_pub.socket.closed)
        a = assert_false(self.test_proxy.xsubsocket.closed)
        b = assert_false(self.test_pub.socket.closed)
        self.test_pub.close()
        #print assert_true(self.test_pub.socket.closed)
        c = assert_true(self.test_pub.socket.closed)
        if a and b and c:
            print "...PASS..."
        else:
            print "...FAIL..."

    def test_proxy_subscriber(self):
        #Test sockets of proxy-subscriber
        print "#############################################"
        print "Test sockets of proxy-subscriber"
        #print assert_false(self.test_proxy.xpubsocket.closed)
        #print assert_false(self.test_sub.socket.closed)
        a = assert_false(self.test_proxy.xpubsocket.closed)
        b = assert_false(self.test_sub.socket.closed)
        self.test_sub.close()
        #print assert_true(self.test_sub.socket.closed)
        c = assert_true(self.test_sub.socket.closed)
        if a and b and c:
            print "...PASS..."
        else:
            print "...FAIL..."

    def test_history(self):
        print "#############################################"
        print "Test the history function"
        msg_coming = ["test_msg"]*10
        history = 3
        h_vec = [[]]
        for i in range(0, len(msg_coming)):
            h_vec = self.test_proxy.history_vector(h_vec, 0, history, msg_coming[i])
        #print assert_equal(history, len(h_vec[0]))
        a = assert_equal(history, len(h_vec[0]))
        if a: 
            print "...PASS..."
        else:
            print "...FAIL..."

    def test_onwership(self):
        print "#############################################"
        print "Test ownership function and publisher disconnected"
        ownership_coming = [3,4,5,5,5,4,4,3,4,4,4]
        strength_vec = []
        cur_strength = 0
        pre_strength = 0
        cur_ind = 0
        count = 0
        num = 3
        # The following codes deal with management of different publishers
        # Note that since the publisher with onwership 5 is discontious, the max_ownership
        # here should be 4 
        for i in range(0, len(ownership_coming)):
            ownership = ownership_coming[i]
            if ownership not in strength_vec:
                strength_vec.append(ownership)
            else:
                curInd = strength_vec.index(ownership)
            if ownership > cur_strength:
                pre_strength = cur_strength
                cur_strength = ownership
                count = 0
            elif ownership == cur_strength:
                count = 0
            else:
                count += 1
                if count >= num:
                    cur_strength = pre_strength
                    count = 0
        #print cur_strength
        #print assert_equal(cur_strength, 4)
        a = assert_equal(cur_strength, 4)
        if a: 
            print "...PASS..."
        else:
            print "...FAIL..."

if __name__ == '__main__':
    #unittest.main()
    test = Test()
    test.test_proxy_publisher()
    test.test_proxy_subscriber()
    test.test_history()
    test.test_onwership()