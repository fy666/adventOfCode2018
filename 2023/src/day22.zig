const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day22.txt");
const fileDataEx = @embedFile("./files/day22ex.txt");

const Regex = @import("zig-regex").Regex;

const Allocator = std.mem.Allocator;
fn line_intersect(comptime T: type, x1: T, y1: T, x2: T, y2: T) bool {
    if (x1 >= x2 and y1 <= y2) {
        return true;
    }
    if (x2 >= x1 and y2 <= y1) {
        return true;
    }
    if (x1 <= y2 and y1 >= y2) {
        return true;
    }
    if (x2 <= y1 and y2 >= y1) {
        return true;
    }
    return false;
}
const Cube = struct {
    name: []const u8,
    supports: std.ArrayList([]const u8),
    p1: [3]u32,
    p2: [3]u32,
    is_supported_by: std.StringHashMap(bool),
    is_supported_by_tmp: std.StringHashMap(bool),

    pub fn init(allocator: Allocator, name: []const u8) Cube {
        return Cube{ .name = name, .p1 = [3]u32{ 0, 0, 0 }, .p2 = [3]u32{ 0, 0, 0 }, .supports = std.ArrayList([]const u8).init(allocator), .is_supported_by = std.StringHashMap(bool).init(allocator), .is_supported_by_tmp = std.StringHashMap(bool).init(allocator) };
    }

    pub fn intersect(self: Cube, other: Cube) bool {
        return line_intersect(u32, self.p1[0], self.p2[0], other.p1[0], other.p2[0]) and line_intersect(u32, self.p1[1], self.p2[1], other.p1[1], other.p2[1]);
    }

    pub fn reset(self: *Cube) !void {
        self.is_supported_by_tmp.clearAndFree();
        var it = self.is_supported_by.iterator();
        while (it.next()) |obj| {
            try self.is_supported_by_tmp.put(obj.key_ptr.*, false);
        }
    }

    pub fn addToGround(self: *Cube, cubes: []Cube) void {
        var zmin: u32 = 1;
        for (cubes) |cube| {
            if (self.intersect(cube)) {
                zmin = @max(zmin, @max(cube.p1[2], cube.p2[2]) + 1);
            }
        }
        var offset = @min(self.p1[2], self.p2[2]);
        self.p1[2] = self.p1[2] - offset + zmin;
        self.p2[2] = self.p2[2] - offset + zmin;
    }

    pub fn fill_supports(self: *Cube, cubes: []Cube) !void {
        for (cubes) |*cube| {
            if (cube == self) {
                continue;
            }
            if ((self.p2[2] == cube.p1[2] - 1) and self.intersect(cube.*)) {
                try self.supports.append(cube.name);
                try cube.is_supported_by.put(self.name, false);
            }
        }
    }
};

fn reset_cubes(
    cubes: *std.StringHashMap(Cube),
) !void {
    var it = cubes.iterator();
    while (it.next()) |obj| {
        try obj.value_ptr.*.reset();
    }
}

fn printStringHashMap(data: std.StringHashMap(bool)) void {
    var it = data.iterator();
    while (it.next()) |item| {
        std.debug.print("{s},", .{item.key_ptr.*});
    }
}

// should return true if a < b :)
fn cmpFunc(context: void, a: Cube, b: Cube) bool {
    _ = context;
    var a_z = @min(a.p1[2], a.p2[2]);
    var b_z = @min(b.p1[2], b.p2[2]);
    return a_z < b_z;
}

fn parse_cube(
    line: []const u8,
    counter: usize,
    allocator: Allocator,
    cubes: *std.ArrayList(Cube),
) !void {
    var re = try Regex.compile(allocator, "(\\d+),(\\d+),(\\d+)~(\\d+),(\\d+),(\\d+)");
    var captures = try re.captures(line);
    if (captures != null) {
        var cube = Cube.init(allocator, try std.fmt.allocPrint(allocator, "{}", .{counter}));
        for (0..3) |ix| {
            cube.p1[ix] = try std.fmt.parseInt(u32, captures.?.sliceAt(ix + 1).?, 10);
            cube.p2[ix] = try std.fmt.parseInt(u32, captures.?.sliceAt(ix + 4).?, 10);
        }
        try cubes.append(cube);
    } else {
        std.debug.print("{s} not found\n", .{line});
        unreachable;
    }
}

fn chain_reaction(cubes: *std.StringHashMap(Cube), allocator: Allocator, first: []const u8) !i32 {
    var counter: i32 = 0;
    const QueueType = std.ArrayList([]const u8);
    var queue = QueueType.init(allocator);
    try queue.append(first);

    while (queue.items.len > 0) {
        var item = queue.orderedRemove(0);
        counter += 1;
        var cube = cubes.get(item).?;
        for (cube.supports.items) |supported| {
            var supported_cube = cubes.getPtr(supported).?;
            _ = supported_cube.is_supported_by_tmp.remove(item);
            if (supported_cube.is_supported_by_tmp.count() == 0) {
                try queue.append(supported_cube.name);
            }
        }
    }
    return counter - 1;
}

fn solve(data: anytype) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();

    var splitsLines = std.mem.split(u8, data, "\n");

    var cubes = std.ArrayList(Cube).init(allocator);
    var counter: usize = 0;
    while (splitsLines.next()) |l| : (counter += 1) {
        try parse_cube(l, counter, allocator, &cubes);
    }

    std.debug.print("{} cubes found \n", .{cubes.items.len});
    std.sort.insertion(Cube, cubes.items, comptime {}, comptime cmpFunc);

    // Add to ground
    for (cubes.items, 0..) |*cube, ix| {
        cube.addToGround(cubes.items[0..ix]);
    }
    std.sort.insertion(Cube, cubes.items, comptime {}, comptime cmpFunc);

    for (cubes.items) |*cube| {
        try cube.fill_supports(cubes.items);
    }

    // for (cubes.items) |cube| {
    //     std.debug.print("Cube {s}: {any} -> {any} is supported by {}, supports {}\n", .{ cube.name, cube.p1, cube.p2, cube.is_supported_by.count(), cube.supports.count() });
    // }

    // Part 1
    var only_support = std.StringHashMap(bool).init(allocator);
    for (cubes.items) |cube| {
        if (cube.is_supported_by.count() == 1) {
            var it = cube.is_supported_by.iterator();
            try only_support.put(it.next().?.key_ptr.*, false);
        }
    }
    var could_be_removed = cubes.items.len - only_support.count();
    std.debug.print("Part 1: {} cubes could be dissintegrated\n", .{could_be_removed});

    // Pärt 2
    var cube_hash = std.StringHashMap(Cube).init(allocator);
    for (cubes.items) |cube| {
        try cube_hash.put(cube.name, cube);
    }

    var part2: i32 = 0;
    for (cubes.items) |cube| {
        try reset_cubes(&cube_hash);
        var fallen = try chain_reaction(&cube_hash, allocator, cube.name);
        //std.debug.print("Removing {s} -> {} cube falls \n", .{ cube.name, fallen });
        part2 += fallen;
    }
    std.debug.print("Part 2: {} \n", .{part2});
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 22: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }

    try solve(if (example) fileDataEx else fileData);
}
