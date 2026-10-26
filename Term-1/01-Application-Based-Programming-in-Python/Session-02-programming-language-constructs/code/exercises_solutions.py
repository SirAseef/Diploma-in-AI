"""Session 02 practice solutions."""

# 1 multiplication table of 7
for i in range(1, 11):
    print(f"7 x {i} = {7 * i}")

# 2 largest without max()
nums = [12, 7, 3, 18, 25, 4]
largest = nums[0]
for n in nums:
    if n > largest:
        largest = n
print("Largest:", largest)
assert largest == 25

# 3 FizzBuzz
for n in range(1, 21):
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)

# 4 vowels
text = "Artificial Intelligence"
vowels = sum(1 for ch in text.lower() if ch in "aeiou")
print("Vowels:", vowels)
assert vowels == 10
