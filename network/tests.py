from django.test import Client, TestCase
from .models import User,Post,Relationship,Profile
import os
import pathlib
import unittest

#mport time
#from selenium import webdriver
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.common.by import By

# Create your tests here.

# Finds the Uniform Resourse Identifier of a file
#def file_uri(filename):
    #return pathlib.Path(os.path.abspath(filename)).as_uri()

# Sets up web driver using Google chrome
#driver = webdriver.Chrome()

#class WebPageTests(unittest.TestCase):
    #def test_title(self):
       # """"Make sure page title is correct"""
        #driver.get(file_uri("templates/network/layout.html"))
        #self.assertEqual(driver.title, "{% block title %}Social Network{% endblock %}")

    #def test_follow_button(self):
       # """"To make sure the follow and unfollow button works correctly"""
       # driver.get(file_uri("templates/network/index.html"))
       # profile = driver.find_element(By.ID, "author-link")
       # profile.click()
        #time.sleep(3)
        #follow_button = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.ID, "follow-button"))
        #follow_button = driver.find_element(By.ID, "follow-button")
        #follow_button.click()
       # self.assertEqual(follow_button.text, "Unfollow")

class TestRelationship(TestCase):
    def setUp(self):
        username = "codeguru"
        email = "codeguru@gmail.com"
        password = "12345678"
        user1 = User.objects.create_user(username, email, password)
        
        username2 = "pthyoncoder"
        email2 = "pthyoncoder@yahoo.com"
        password2 = "abcdefgh"
        user2 = User.objects.create_user(username2, email2, password2)

        friends = Relationship.objects.create(follows = user1, follow_by = user2)

    def test_follows_count(self):
        user = User.objects.get(username = "codeguru")
        friend = Relationship.objects.filter(follows = user)
        self.assertAlmostEqual(friend.count(), 1)
    
    def test_follow_by_count(self):
        user = User.objects.get(username = "pthyoncoder")
        friend = Relationship.objects.filter(follow_by = user)
        self.assertAlmostEqual(friend.count(), 1)

    def test_valid_relationship(self):
        user1 = User.objects.get(username = "codeguru")
        user2 = User.objects.get(username = "pthyoncoder")
        friend = Relationship.objects.get(follows = user1, follow_by = user2)
        self.assertTrue(friend.is_valid_friend())

    def test_not_valid_relationship(self):
        user1 = User.objects.get(username = "codeguru")
        user2 = User.objects.get(username = "pthyoncoder")
        friend2 = Relationship.objects.get(follows = user1, follow_by = user2)
        self.assertFalse(friend2.is_not_valid_friend())

#if __name__ == "__main__":
   #unittest.main()
