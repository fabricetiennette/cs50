#include <stdbool.h>
#include <stdlib.h>
#include <string.h>     
#include <strings.h>    
#include <stdio.h>      
#include <ctype.h>      
#include "dictionary.h"

#define HASHTABLE_SIZE 16384
#define MEANING_OF_LIFE 42 

typedef struct Node
{
    char word[LENGTH+1];
    struct Node* next;
}Node;

Node* hashtable[HASHTABLE_SIZE];

unsigned int numWords = 0;

int hash_it(const char* needs_hashing)
{
    unsigned int hash = 0;
    for (int i=0, n=strlen(needs_hashing); i<n; i++)
        hash = (hash << 2) ^ needs_hashing[i];
    return hash % HASHTABLE_SIZE;
}
 
unsigned int jenkins_hash(char *key)
{
    unsigned int hash, i;
    for(hash = i = 0; i < strlen(key); ++i)
    {
        hash += key[i];
        hash += (hash << 10);
        hash ^= (hash >> 6);
    }
    hash += (hash << 3);
    hash ^= (hash >> 11);
    hash += (hash << 15);
    return hash % HASHTABLE_SIZE;
}

unsigned int djb2_hash(char *str)
{
    unsigned long hash = 5381;
    int c;
    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c;
    }
    return hash % HASHTABLE_SIZE;
}
 
void freeList(struct Node* currentNode)
{
    if(currentNode->next != NULL) { freeList(currentNode->next); }
    free(currentNode);
}

char* strLower( char* str ) {
  char *temp = NULL;
 
  for ( temp = str; *temp; temp++ ) {
    *temp = tolower( *temp );
  }
 
  return str;
}

bool check(const char* word)
{

    char* lower_word;
    lower_word = (char*)malloc(strlen(word) + 1); 
    strcpy(lower_word,word);
    lower_word = strLower(lower_word); 
    int lower_hashvalue = djb2_hash(lower_word);
    free(lower_word); 

    if(hashtable[lower_hashvalue] == NULL)
    {
        return false;
    } else 
    {
        Node* searcher = hashtable[lower_hashvalue]; 
        do{
            if(strcasecmp(searcher->word,word) == 0) {return true;} 
            searcher = searcher->next; 
        }while(searcher != NULL); 
    }
    return false;
}

bool load(const char* dictionary)
{
    
    FILE* dptr = fopen(dictionary, "r"); 
    if(dptr == NULL) 
    {
        printf("Unable to load the dictionary file.\n");
        return false;
    }
    
    char currentWord[LENGTH+1]; 
    int index = 0;
    for (int c = fgetc(dptr); c != EOF; c = fgetc(dptr)) 
    {
        if(isalpha(c) || c == '\'')  
        {
            currentWord[index] = c;
            index++;
        } 
        else
        {
            currentWord[index] = '\0'; 
            index = 0;
            int hashvalue = djb2_hash(currentWord); 
            
            Node* newNode = malloc(sizeof(Node));
            if(newNode == NULL) {
                printf("unable to complete malloc() of new node\n");
                return false;
            }
            strcpy(newNode->word, currentWord);
            numWords++;
            if(hashtable[hashvalue] == NULL) 
            {
                
                hashtable[hashvalue] = newNode;
            }
            else 
            {
                
                newNode->next = hashtable[hashvalue];
                hashtable[hashvalue] = newNode;
            }
        }
    }
  
    fclose(dptr);
    return true;
}

void nodesPrint(void)
{
    for(int i = 0; i < HASHTABLE_SIZE; i++)
    {
        if(hashtable[i] == NULL) {
            printf("hashtable[%d] is null\n",i);
        } else {
            printf("hashtable[%d]",i);
            Node* searcher = hashtable[i];
            do{
                printf("-%s-",searcher->word);
                searcher = searcher->next;
                  
            }while(searcher != NULL);
            printf("\n");
        }
    }
}


unsigned int size(void)
{
    return numWords;
}

bool unload(void)
{
   
    for(int i = 0; i < HASHTABLE_SIZE; i++)
        
        if(hashtable[i] != NULL)
        {
            Node* ucursor = hashtable[i];
            freeList(ucursor);
        }
    
    return true;
}