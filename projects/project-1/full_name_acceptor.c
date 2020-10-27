/*
Inspired by <https://stackoverflow.com/questions/1085083/regular-expressions-in-c-examples>
*/

#include <regex.h>
#include <stdio.h>
#include <stdlib.h>

int main(){

	regex_t regex;
	int ret;
	char message[100];
	char input[100];
	
	const char * regex_string = "(^[A-Z][[:alpha:]]+)([[:space:]][A-Z]\\.?)?([[:space:]][A-Z][[:alpha:]]+)([[:space:]](Jr\\.|I{1,3}|Sr\\.))?";

	/*
	Regex Explanation
	-----------------
	- (^[A-Z][[:alpha:]]+) : Matches one or more  capitalized, alphabetic words at the start of a string
	- ([[:space:]][A-Z]\\.?)? : Matches zero or one of a space, followed by a capital letter, optionally followed by a period
	- ([[:space:]][A-Z][[:alpha:]]+) : Matches one or more last names with a preceding space, and a capital letter at the start of the name
	- ([[:space:]](Jr\\.|I{1,3}|Sr\\.))? : matches either one or zero of {Jr., Sr., I, II, III}
	*/

	// Compile our regex string
	ret = regcomp(&regex, regex_string, REG_EXTENDED);
	if (ret){
		puts("Error Compiling Regex");
		exit(1);
	}

	// Get user input
	puts("Please enter your full name:");
	fgets(input, 100, stdin);

	// Execute the regex we compiled against input
	ret = regexec(&regex, input, 0, NULL, 0);
	if (!ret){
		puts("Name matched regex");
	}
	else if (ret==REG_NOMATCH){
		puts("Name did not match regex");
	}
	else{
		regerror(ret, &regex, message, sizeof(message));
		fprintf(stderr, "Regex match failed: %s\n", message);
		exit(1);
	}

	exit(0);
}