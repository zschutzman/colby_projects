/*
Name: Zach Schutzman
File: Cell.java
Course: CS231, Project 4
Created: 9/16/2014
Modified: 9/30/2014
*/


import java.util.ArrayList;
import java.awt.Graphics;
/* A cell object used to simulate a Game of Life. */
public abstract class Cell{

	protected double y;
	protected double x;
	
	
	/* A constructor method that creates a cell at a specified x-y coordinate
	   location.
	*/
	public Cell(double x0, double y0){
	
		this.y = y0;
		this.x = x0;
	}
	
	
	/* Returns the Cell's x location. */
	public double getX(){
		return this.x;
	}
	
	
	/* Returns the Cell's y location. */
	public double getY(){
		return this.y;
	}	
	
	
	/* Rounds the x coordinate to the nearest integer to return a "column" location. */
	public int getCol(){
		return (int) Math.round(this.x);
	}
	
	
	/* Rounds the y coordinate to the nearest integer to return a "row" location. */
	public int getRow(){
		return (int) Math.round(this.y);	
	}
	

	/* Allows a Cell to be moved by given amounts. */
	public void move(double dx, double dy){
	
		this.x = this.x + dx;
		this.y = this.y + dy;
	}
	
	
	/* Returns each Cell as a string containing only a period. */
	public String toString(){
		
		return ".";	
	}
	
	

	
	public abstract boolean isNeighbor(Cell cell);
	public abstract void updateState(ArrayList<Cell> neighbors);
	public abstract void draw(Graphics g, int x, int y, int scale);
	
}