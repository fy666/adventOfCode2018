const MyErr = error{OusideMatrix};
pub const Point2D = struct {
    x: i32,
    y: i32,
    pub fn new(x: anytype, y: anytype) Point2D {
        switch (@TypeOf(x)) {
            i32 => return Point2D{ .x = x, .y = y },
            usize => return Point2D{ .x = @intCast(x), .y = @intCast(y) },
            else => unreachable,
        }
    }

    pub fn add(self: *const Point2D, other: *const Point2D) Point2D {
        return Point2D{ .x = self.x + other.x, .y = self.y + other.y };
    }

    pub fn getX(self: *const Point2D, max_bound: usize) !usize {
        if (self.x < 0 or self.x >= max_bound) {
            return MyErr.OusideMatrix;
        }
        return @intCast(self.x);
    }
    pub fn getY(self: *const Point2D, max_bound: usize) !usize {
        if (self.y < 0 or self.y >= max_bound) {
            return MyErr.OusideMatrix;
        }
        return @intCast(self.y);
    }
};

pub fn getDirections() [8]Point2D {
    var res: [8]Point2D = undefined;
    var index: usize = 0;
    for (0..3) |x| {
        for (0..3) |y| {
            if (x != 1 or y != 1) {
                res[index] = Point2D.new(@as(i32, @intCast(x)) - 1, @as(i32, @intCast(y)) - 1);
                index += 1;
            }
        }
    }
    return res;
}
