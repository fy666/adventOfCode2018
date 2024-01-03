const std = @import("std");
const Regex = @import("zig-regex").Regex;

const MyErr = error{OusideMatrix};
pub const Point2D = struct {
    x: i32,
    y: i32,
    pub fn new(x: anytype, y: anytype) Point2D {
        switch (@TypeOf(x)) {
            i32 => return Point2D{ .x = x, .y = y },
            usize => return Point2D{ .x = @intCast(x), .y = @intCast(y) },
            comptime_int => return Point2D{ .x = @intCast(x), .y = @intCast(y) },
            else => {
                std.debug.print("Type of data = {s}\n", .{@typeName(@TypeOf(x))});
                unreachable;
            },
        }
    }

    pub fn add(self: *const Point2D, other: *const Point2D) Point2D {
        return Point2D{ .x = self.x + other.x, .y = self.y + other.y };
    }

    pub fn getManhattanDistance(self: *const Point2D, other: *const Point2D) i32 {
        return @intCast(@abs(self.x - other.x) + @abs(self.y - other.y));
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

pub fn customEquality(a: anytype, b: anytype) bool {
    switch (@TypeOf(a)) {
        Point2D => return (a.x == b.x and a.y == b.y),
        else => unreachable,
    }
    unreachable;
}

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

pub fn get4Directions() [4]Point2D {
    var res: [4]Point2D = undefined;
    var index: usize = 0;
    for (0..3) |x| {
        for (0..3) |y| {
            if ((x + y) % 2 == 1) {
                res[index] = Point2D.new(@as(i32, @intCast(x)) - 1, @as(i32, @intCast(y)) - 1);
                index += 1;
            }
        }
    }
    return res;
}

pub fn get_match(comptime T: type, line: []const u8) !?T {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var re = try Regex.compile(allocator, "(-?\\d+)");

    var captures = try re.captures(line);
    var result: ?T = null;
    //std.debug.print("captures = {}\n", .{captures.?.len()});
    if (captures != null) {
        var cap = captures.?.sliceAt(1);
        result = try std.fmt.parseInt(T, cap.?, 10);
    }
    return result;
}

pub fn get_all_numbers(comptime T: type, line: []const u8, values: *std.ArrayList(T)) !void {
    var split_numbers = std.mem.splitAny(u8, line, " ,");
    while (split_numbers.next()) |num_str| {
        var res = try get_match(T, num_str);
        if (res != null) {
            try values.append(res.?);
            //std.debug.print("{s} -> {} \n", .{ num_str, res.? });
        }
    }
    //std.debug.print("{s} -> {any} \n", .{ line, values.items });
}

pub fn sum(comptime T: type, data: []T) T {
    var res: T = 0;
    for (data) |x| {
        res += x;
    }
    return res;
}
