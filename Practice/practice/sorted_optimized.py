class Solution:
    def validateCoupons(self, code, businessLine, isActive):
        order = ["electronics", "grocery", "pharmacy", "restaurant"]
        valid_business = set(order)

        grouped = {b: [] for b in order}

        for coupon, business, active in zip(code, businessLine, isActive):
            if not active:
                continue

            if business not in valid_business:
                continue

            if not coupon:
                continue

            if not all(c.isalnum() or c == '_' for c in coupon):
                continue

            grouped[business].append(coupon)

        # Sort inside each business line
        result = []
        for b in order:
            result.extend(sorted(grouped[b]))

        return result
