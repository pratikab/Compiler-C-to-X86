#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

struct module {
   int data;
   int key;
   struct module *next;
};

struct module *head = NULL;
struct module *current = NULL;

void printList() {
   struct module *ptr = head;
   printf("\n[ ");
	
   while(ptr != NULL) {
      printf("(%d,%d) ",ptr->key,ptr->data);
      ptr = ptr->next;
   }
	
   printf(" ]");
}


struct module * deleteFirst() {

   struct module *tempLink = head;
	
   head = head->next;
	
   return tempLink;
}

bool isEmpty() {
   return head == NULL;
}

int length() {
   int length = 0;
   struct module *current;
	
   for(current = head; current != NULL; current = current->next) {
      length++;
   }
	
   return length;
}

struct module * find(int key) {

   struct module * current = head;

   if(head == NULL) {
      return NULL;
   }

   while(current->key != key) {
	
      if(current->next == NULL) {
         return NULL;
      } else {
         current = current->next;
      }
   }      
	
   return current;
}

struct module * delete(int key) {

   struct module * current = head;
   struct module * previous = NULL;
	
   if(head == NULL) {
      return NULL;
   }

   while(current->key != key) {

      if(current->next == NULL) {
         return NULL;
      } else {
         previous = current;
         current = current->next;
      }
   }

   if(current == head) {
      head = head->next;
   } else {
         previous->next = current->next;
   }    
	
   return current;
}

void sort() {

   int i, j, k, tempKey, tempData;
   struct module *current;
   struct module *next;
	
   int size = length();
   k = size ;
	
   for ( i = 0 ; i < size - 1 ; i++) {
      current = head;
      next = head->next;
		
      for ( j = 1 ; j < k ; j++ ) {   
		
         if ( current->data > next->data ) {
            tempData = current->data;
            current->data = next->data;
            next->data = tempData;

            tempKey = current->key;
            current->key = next->key;
            next->key = tempKey;
         }
			
         current = current->next;
         next = next->next;
      }
   }   
}

void reverse(struct module ** head_ref) {
   struct module * prev   = NULL;
   struct module * current = *head_ref;
   struct module * next;
	
   while (current != NULL) {
      next  = current->next;
      current->next = prev;   
      prev = current;
      current = next;
   }
	
   *head_ref = prev;
}

int main() {
   insertFirst(1,10);
   insertFirst(2,20);
   insertFirst(3,30);
   insertFirst(4,1);
   insertFirst(5,40);
   insertFirst(6,56); 

   printf("Original List: "); 
	
   printList();

   while(!isEmpty()) {
      struct module *temp = deleteFirst(4);
      printf("\nDeleted value:");
      printf("(%d,%d) ",temp->key,temp->data);
   }  
	
   printf("\nList after deleting all items: ");
   printList();
   insertFirst(1,10);
   insertFirst(2,20);
   insertFirst(3,30);
   insertFirst(4,1);
   insertFirst(5,40);
   insertFirst(6,56);
   
   printf("\nRestored List: ");
   printList();
   printf("\n");  

   struct module *foundLink = find(4);
	
   if(foundLink != NULL) {
      printf("Element found: ");
      printf("(%d,%d) ",foundLink->key,foundLink->data);
      printf("\n");  
   } else {
      printf("Element not found.");
   }

   delete(4);
   printf("List after deleting an item: ");
   printList();
   printf("\n");
   foundLink = find(4);
	
   if(foundLink != NULL) {
      printf("Element found: ");
      printf("(%d,%d) ",foundLink->key,foundLink->data);
      printf("\n");
   } else {
      printf("Element not found.");
   }
	
   printf("\n");
   sort();
	
   printf("List after sorting the data: ");
   printList();
	
   reverse(&head);
   printf("\nList after reversing the data: ");
   printList();
}