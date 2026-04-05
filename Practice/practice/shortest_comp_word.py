class Solution:
    def shortestCompletingWord(self, licensePlate: str, words: list[str]) -> str:
        out = []
        plate_chr = []
        plate_list = list(licensePlate)
        for char in plate_list:
            if char.isalpha():
                plate_chr.append(char)
        for char in plate_chr:
            ...


solution = Solution()
invoke = solution.shortestCompletingWord(licensePlate = "1s3 PSt", words = ["step","steps","stripe","stepple"])
print(invoke)