
console.log("Script started!!!!"); // Print to console
// Single line Comments:

/*
Multiline comment

*/

// Variable declarations:

// Recommended way:
const MAX_TEMP = 222;
let myName = "Hail"; // Block scope {}

// Auto:
a = 222; // Implicit var

// Old way 
var myCounter = 0; // Function scope, window object property, module scope, ....

// MAX_TEMP = 222 // script.js:21 Uncaught TypeError: Assignment to constant variable.

// typeof operator
console.log(typeof MAX_TEMP)
// Data types:
/*
Type	Description
String	A text of characters enclosed in quotes
Number	A number representing a mathematical value
Bigint	A number representing a large integer
Boolean	A data type representing true or false
Object	A collection of key-value pairs of data
Undefined	A primitive variable with no assigned value
Null	A primitive value representing object absence
Symbol	A unique and primitive identifier

*/

// JS Operators
/*
Arithmetic Operators
Operator	Description
+	        Addition
-	        Subtraction
*	        Multiplication
**	        Exponentiation
/	        Division
%	        Modulus (Division Remainder)

++	        Increment
--	        Decrement
Prefix form / Suffix form


Assignment Operators
Operator	Example	    Same As
=	        x = y	    x = y
+=	        x += y	    x = x + y
-=	        x -= y	    x = x - y
*=	        x *= y	    x = x * y
/=	        x /= y	    x = x / y
%=	        x %= y	    x = x % y
**=	        x **= y	    x = x ** y


Comparison Operators
Operator	Description	                         Example
==	        equal to	                            x == 5
===	        equal value and equal type	            x === 5
!=	        not equal	                            x != 5
!==	        not equal value or not equal type	    x !== 5
>	        greater than	                        x > 5
<	        less than	                            x < 5
>=	        greater than or equal to	            x >= 5
<=	        less than or equal to	                x <= 5


Logical Operators
Operator	Description
&&	        logical and
||	        logical or
!	        logical not


*/

// if operator

/*
if (condition1) {
    // True statements
    
} else if (condition2){
    // False statements
    
} else {

}


if (condition) {
    // True statements
    
} else {
    // False statements
    
}

if (condition) {
    // True statements
    
}

*/

// String
""
''

// back tick - multiline string (with string interpolation option)
`
Text 
${a}  -> string interpolation

`


