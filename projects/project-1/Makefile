all:
	gcc -o full_name_acceptor -Werror full_name_acceptor.c

clean:
	rm full_name_acceptor

test: test_py test_sh test_c
	echo "Tested All Targets."

test_sh:
	echo "Testing email_acceptor.sh"

	echo "\n = [email] Passing"
	-./email_acceptor.sh test_email@provider.site.nz

	echo "\n = [email] Failing"
	-./email_acceptor.sh tes%il@provider.site

test_py:
	echo "Testing password_acceptor.py"

	echo "\n = [password] Passing"
	-echo 'goodP4$sW0rD1@3$' | ./password_acceptor.py

	echo "\n = [password] Failing"
	-echo 'tooshort' | ./password_acceptor.py

test_c: clean all
	echo "Testing full_name_acceptor.c"

	echo "\n = [full_name] Passing"
	-echo 'This B. Agoodname Sr.' | ./full_name_acceptor

	echo "\n = [full_name] Failing"
	-echo 'This _ISN t. Good Sr.' | ./full_name_acceptor


