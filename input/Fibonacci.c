int Fibonacci(int amount_of_iterations) {
int previous = 0;
int current = 1;

for (int i = 0; i < amount_of_iterations; i = i + 1) {
int result = previous + current;
previous = current;
current = result;
}
return current;
}

int main() {
int fib_result = Fibonacci(20);

printf(fib_result);
}