class Solution:
    def validateCoupons(self, code, businessLine, isActive):
        result = []
        invalid_icon = "@"
        order = ["electronics", "grocery", "pharmacy", "restaurant"]
        valid_business = set(order)

        grouped = {b: [] for b in order}
        for i in range(len(code)):
            coupoun, buissness, active = code[i], businessLine[i], isActive[i]
            if active and coupoun and buissness.lower() in ("restaurant","grocery","pharmacy","restaurant","electronics") and invalid_icon not in coupoun:
                grouped[buissness].append(coupoun)
        for b in order:
            result.extend(sorted(grouped[b]))
        return result

solution = Solution()
invoke = solution.validateCoupons(["Qf8NjqOTYp","w4xOTEM20C"], 
                                  ["pharmacy","pharmacy"],
                                  [True, True])

print(invoke)