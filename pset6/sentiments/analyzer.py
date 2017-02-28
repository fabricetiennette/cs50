import nltk
import os
import sys

class Analyzer():
    """Implements sentiment analysis."""
    
    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        
        self.positives = positives
        self.negatives = negatives
        self.positive_words = []
        self.negative_words = []
        
        with open(self.positives, 'r') as p:
            for lines in p:
                if not lines.startswith(';') and not lines.startswith('\n'):
                    self.positive_words.append(lines.strip('\n'))
            
        with open(self.negatives, 'r') as n:
            for lines in n:
                if not lines.startswith(';') and not lines.startswith('\n'):
                    self.negative_words.append(lines.strip('\n'))
                    
    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        
        
        score = 0
        
        tokenizer = nltk.tokenize.TweetTokenizer()
        
        tokens = tokenizer.tokenize(text)
        
        for token in tokens:
            if token.lower() in self.positive_words:
                score += 1
            elif token.lower() in self.negative_words:
                score -= 1
                
        return score