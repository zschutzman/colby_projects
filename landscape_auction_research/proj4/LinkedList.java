/*
Name: Zach Schutzman
File: LinkedList.java
Course: CS231, Project 4
Created: 9/23/2014
Modified: 9/30/2014
*/

import java.util.*;


/* Implements an iterable Linked List data structure which consists of Nodes with
   data and a Next pointer to indicate the next item in the list.
*/
public class LinkedList<T> implements Iterable<T>{

	/* A private subclass to define the Node structure within the Linked List. */
	private class Node{
	
		private Node next;
		private T field;
		
		/* A constructor which makes a new Node with a given value in its data field. */
		public Node(T item){
		
			this.next = null;
			this.field = item;		
		}
		
		/* Returns the data stored in a Node. */
		public T getThing(){
			return this.field;
		}
		
		/* Adjusts the pointer of a Node to point to the given next Node. */
		public void setNext(Node n){
			this.next = n;	
		}
		
		/* Returns the Node that this Node is pointing to. */
		public Node getNext(){
			return this.next;	
		}
	
		/* Returns the number of Nodes which follow the current Node in the list. */
		public int length(){
			if (this.next == null){
        	    return 0;
       		} else {
       	    	 return 1 + this.next.length();
        	} 
        }
	}


	private Node head;
	
	
	/* The constructor for the LinkedList object which creates a new head node which
	   points to nothing.
	*/
	public LinkedList(){
		this.head = new Node(null);
	}
	
	/* Deletes everything in the LinkedList by readjusting the head to point to nothing.
	  Automatic garbage collection deletes whatever list existed before.
	*/
	public void clear(){
		this.head = new Node(null);
	}

	/* Returns the number of Nodes in the LinkedList by recursively asking each
	   Node how many Nodes follow it.
	*/
	public int size(){
		return this.head.length();
	}
	
	/* Creates a new Node with the given data field and adds it at the front of the list. */
	public void add(T item){
	
		Node newNode = new Node(item);
		newNode.next = this.head;
		this.head = newNode;
	}
	
	/* Removes the first instance of a given piece of data in the list, 
	   and returns true if the data is found and removed.  Otherwise, leaves the 
	   list unchanged and returns false.
	*/
	public boolean remove(Object obj){
		
		if (this.head.field.equals(obj)){
			this.head = this.head.next;
			return true;
		} else {
		
		Node current = this.head;
		Node follow = this.head.next;
		for (int i=0; i<this.size(); i++){
			if (obj.equals(follow.field)){
				current.next = follow.next;
				return true;
			}
			current = current.next;
			follow = follow.next; 
		}
		return false;
		}
	}
				
				

	/* A subclass that allows for the LinkedList to be iterable (for each loops). */
	private class LLIterator implements Iterator<T>{
	
		private Node heldNode;
		
		/* A constructor which points the LLIterator to the list's head. */
		public LLIterator(Node head){
			this.heldNode = head;
		}
		
		/* Checks if the Node that the LLIterator is pointing to has another Node
		   following it. 
		*/
		public boolean hasNext(){
	
			if (this.heldNode.next == null){		
				return false;
				
			} else {
				return true;
			}
		}
		
		
		/* Points the LLIterator to the next Node. */
		public T next(){
		
			T nextItem = this.heldNode.getThing();
			this.heldNode = this.heldNode.getNext();
			return nextItem;
		}
		
		
		/* Empty method as it only needs to exist to implement Iterator. */
		public void remove(){}
	
	}
	
	/* Constructs the new LLIterator object to be used on the LinkedList. */
	public  LLIterator iterator(){
	
		LLIterator iter = new LLIterator(this.head);
		return iter;
	}
	
	
	/* Adds each item in the LinkedList to an ArrayList, which is returned. */
	public ArrayList<T> toArrayList(){
		ArrayList<T> arList = new ArrayList<T>();
		
		for(T item: this) {
			arList.add(item);	
		}
		return arList;	
	}
	
	
	/* Calls the toArrayList() method, then shuffles the list into a randomized order,
	   then returns the shuffled list.
	*/
	public ArrayList<T> toShuffledList(){
	
		ArrayList<T> l = this.toArrayList();
		
		ArrayList<T> shuffList = new ArrayList<T>();
		
		Random r = new Random();
		
		for (int i=0; i<l.size(); i++){
			int k = r.nextInt(l.size());
			shuffList.add(l.get(k));
			l.remove(k);
		}
		
		return shuffList;
	}
	

/* A main method used to test various methods in the class. */	
public static void main(String[] argv) {
    LinkedList<Integer> llist = new LinkedList<Integer>();
	
	
	llist.add(5);
	llist.add(10);
	llist.add(20);
	
	System.out.println("ADDED");
	
	System.out.printf("\nAfter setup %d\n", llist.size());
	
	System.out.println("L145");
	
	for(Integer item: llist) {
		System.out.printf("thing %d\n", item);
	}
	
	System.out.println("L151");
	
	llist.clear();
	
	System.out.printf("\nAfter clearing %d\n", llist.size());
	for (Integer item: llist) {
		System.out.printf("thing %d\n", item);
	}

    for (int i=0;i<20;i+=2) {
		llist.add( i );
	}
	
	boolean removed = llist.remove(4);
	System.out.println(removed);

	System.out.printf("\nAfter setting %d\n", llist.size());
	for (Integer item: llist) {
		System.out.printf("thing %d\n", item);
	}
	
	ArrayList<Integer> alist = llist.toArrayList();
	System.out.printf("\nAfter copying %d\n", alist.size());
	for(Integer item: alist) {
		System.out.printf("thing %d\n", item);
	}						

	alist = llist.toShuffledList();
	System.out.printf("\nAfter copying %d\n", alist.size());
	for(Integer item: alist) {
		System.out.printf("thing %d\n", item);
	}
	
	}
	
	
}