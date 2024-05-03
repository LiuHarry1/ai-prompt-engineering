import markdown

# markdown.markdownFromFile(input='xx.md', output='xx.html')

ss = """
 program

Here is a simple "Hello, World!" program in Java:
```
public class HelloWorld {
  public static void main(String[] args) {
    System.out.println("Hello, World!");
  }
}
```
Let me explain what's going on:

* `public class HelloWorld`: This line declares a new public class called `HelloWorld`. In Java, everything is an object, and classes are the blueprints for creating objects.
* `public static void main(String[] args)`: This line declares the `main` method, which is the entry point of the program. The `public` access modifier means that the method can be accessed from outside the class, and the `static` keyword means that the method can be called without creating an instance of the class. The `void` return type means that the method doesn't return any value. The `String[] args` parameter is an array of strings that represents the command-line arguments passed to the program.
* `System.out.println("Hello, World!")`: This line uses the `println` method of the `System.out` object to print the string "Hello, World!" followed by a newline character to the console.

To run this program, you'll need to compile it into a `.class` file using the `javac` command, and then run it using the `java` command. Here are the steps:

1. Save the code in a file called `HelloWorld.java`.
2. Compile the code using the following command:
```
javac HelloWorld.java
```
This will create a `HelloWorld.class` file in the same directory.
3. Run the program using the following command:
```
java HelloWorld
```
This will print "Hello, World!" to the console.

I hope this helps! Let me know if you have any questions.
"""

print(ss)
print(markdown.markdown(ss))