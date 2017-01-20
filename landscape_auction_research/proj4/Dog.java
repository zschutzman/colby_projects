public class Dog extends Animal{
	
		
		public Dog(){
			this.setName("Dog");
		}
		
		public String speak(){
			return "WOOF";
		}
	
	
	
	
	
	public static void main(String[] args){
	
		Dog puppy = new Dog();
		System.out.println(puppy.speak());
	}
}

