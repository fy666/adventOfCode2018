const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day5.txt");
const fileDataEx = @embedFile("./files/day5ex.txt");
const Regex = @import("zig-regex").Regex;

const arrayRangeType = std.ArrayListAligned(Range, null);
const Allocator = std.mem.Allocator;

fn get_match(line: []const u8) ![3]i64 {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var re = try Regex.compile(allocator, "(\\d+) (\\d+) (\\d+)");

    var captures = try re.captures(line);
    var result: [3]i64 = undefined;
    //std.debug.print("captures = {}\n", .{captures.?.len()});
    if (captures != null) {
        for (0..3) |i| {
            var cap = captures.?.sliceAt(i + 1);
            result[i] = try std.fmt.parseInt(i64, cap.?, 10);
        }
    }
    return result;
}

fn get_seeds(line: []const u8) ![3]i64 {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var re = try Regex.compile(allocator, "(\\d+) (\\d+) (\\d+)");

    var captures = try re.captures(line);
    var result: [3]i64 = undefined;
    //std.debug.print("captures = {}\n", .{captures.?.len()});
    if (captures != null) {
        for (0..3) |i| {
            var cap = captures.?.sliceAt(i + 1);
            result[i] = try std.fmt.parseInt(i64, cap.?, 10);
        }
    }
    return result;
}

pub const Range = struct {
    start: i64,
    range: i64,
    add: i64,

    pub fn getCorrespondance(self: *const Range, x: i64) ?i64 {
        if (x >= self.start and x < (self.start + self.range)) {
            return x + self.add - self.start;
        }
        return null;
    }
    pub fn getInvertedCorrespondance(self: *const Range, x: i64) ?i64 {
        if (x >= self.add and x < (self.add + self.range)) {
            return x + self.start - self.add;
        }
        return null;
    }
};

pub const Almanac = struct {
    corresp: arrayRangeType,
    allocator: Allocator,
    cache: std.AutoHashMap(i64, i64),

    pub fn newAlmanac(allocator: Allocator) Almanac {
        var item = Almanac{ .allocator = allocator, .corresp = std.ArrayList(Range).init(allocator), .cache = std.AutoHashMap(i64, i64).init(allocator) };
        return item;
    }

    pub fn addRange(self: *Almanac, start: i64, range: i64, add: i64) !void {
        var item = Range{ .start = start, .range = range, .add = add };
        try self.corresp.append(item);
    }
    pub fn getInvertedCorrespondance(self: *Almanac, x: i64) i64 {
        for (self.corresp.items) |corr| {
            var output = corr.getInvertedCorrespondance(x);
            if (output != null) {
                return output.?;
            }
        }
        return x;
    }
    pub fn getCorrespondance(self: *Almanac, x: i64) i64 {
        for (self.corresp.items) |corr| {
            var output = corr.getCorrespondance(x);
            if (output != null) {
                return output.?;
            }
        }
        return x;
    }
};

fn solve(data: anytype) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();

    var almanach: [7]Almanac = undefined;
    var seeds = std.ArrayList(i64).init(allocator);

    var splits = std.mem.split(u8, data, "\n\n");
    var ix: i32 = 0;
    while (splits.next()) |line| : (ix += 1) {
        if (ix == 0) {
            // seed list
            try utils.get_all_numbers(i64, line, &seeds);
            continue;
        }
        var new_almanach = Almanac.newAlmanac(allocator);
        var almanach_lines = std.mem.split(u8, line, "\n");
        var almanach_line_num: i32 = 0;
        while (almanach_lines.next()) |l| : (almanach_line_num += 1) {
            if (almanach_line_num == 0) {
                // almanach name, pass
                continue;
            }
            // parse 3 ints
            var numbers = try get_match(l);
            try new_almanach.addRange(numbers[1], numbers[2], numbers[0]);
        }
        std.debug.print("New almanach with {} ranges\n", .{new_almanach.corresp.items.len});
        almanach[@intCast(ix - 1)] = new_almanach;
    }
    std.debug.print("{} Seeds = {any}\n", .{ seeds.items.len, seeds.items });

    var best_seed: i64 = undefined;
    for (seeds.items, 0..) |seed, is| {
        var output: i64 = seed;
        for (&almanach) |*alm| {
            output = alm.getCorrespondance(output);
        }
        if (is == 0) {
            best_seed = output;
        }
        best_seed = @min(best_seed, output);
    }
    std.debug.print("Part 1 = {}\n", .{best_seed});

    // PART 2
    var min_wanted_output: i64 = 0;
    finding: while (true) : (min_wanted_output += 1) {
        var al_ix: i64 = almanach.len;
        var input: i64 = min_wanted_output;
        while (al_ix > 0) {
            al_ix -= 1;
            input = almanach[@intCast(al_ix)].getInvertedCorrespondance(input);
        }
        var seed_ix: usize = 0;
        while (seed_ix < seeds.items.len) : (seed_ix += 2) {
            if (input >= seeds.items[seed_ix] and input < seeds.items[seed_ix + 1] + seeds.items[seed_ix]) {
                break :finding;
            }
        }
    }
    std.debug.print("Part 2 = {}\n", .{min_wanted_output});
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 4: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }
    try solve(if (example) fileDataEx else fileData);
}
