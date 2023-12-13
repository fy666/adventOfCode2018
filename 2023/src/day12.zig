const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");
const Point2D = utils.Point2D;

const fileData = @embedFile("./files/day11.txt");
const fileDataEx = @embedFile("./files/day11ex.txt");
const Regex = @import("zig-regex").Regex;

fn expand(galaxies: std.ArrayList(Point2D), expansion: i32) !std.ArrayList(Point2D) {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var result = std.ArrayList(Point2D).init(allocator);

    var max_col: i32 = 0;
    var max_line: i32 = 0;
    for (galaxies.items) |point| {
        max_col = @max(max_col, point.y);
        max_line = @max(max_line, point.x);
    }
    max_col += 1;
    max_line += 1;
    var columns: []i32 = try allocator.alloc(i32, @intCast(max_col));
    var lines: []i32 = try allocator.alloc(i32, @intCast(max_line));
    for (columns, 0..) |_, ic| {
        columns[ic] = 0;
    }
    for (lines, 0..) |_, ic| {
        lines[ic] = 0;
    }

    for (galaxies.items) |point| {
        columns[@intCast(point.y)] = 1;
        lines[@intCast(point.x)] = 1;
    }

    // Expanding columns:
    var cols_to_add: i32 = 0;
    for (columns, 0..) |exp_col, ic| {
        if (exp_col == 0) {
            cols_to_add += (expansion - 1);
        }
        columns[ic] = cols_to_add;
    }

    var lines_to_add: i32 = 0;
    for (lines, 0..) |exp_lines, ic| {
        if (exp_lines == 0) {
            lines_to_add += (expansion - 1);
        }
        lines[ic] = lines_to_add;
    }
    for (galaxies.items, 0..) |point, ip| {
        _ = ip;
        // galaxies.items[ip].x = point.x + lines[@intCast(point.x)];
        // galaxies.items[ip].y = point.y + columns[@intCast(point.y)];
        try result.append(Point2D.new(point.x + lines[@intCast(point.x)], point.y + columns[@intCast(point.y)]));
    }
    return result;
}

fn count_shortest_distances(galaxies: *std.ArrayList(Point2D)) i64 {
    var sum: i64 = 0;
    for (galaxies.items, 0..galaxies.items.len - 1) |p1, index| {
        for (index + 1..galaxies.items.len) |other_index| {
            var d = Point2D.getManhattanDistance(&p1, &galaxies.items[other_index]);
            sum += d;
        }
    }
    return sum;
}

fn solve(data: anytype) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    //var galaxies = std.AutoHashMap(Point2D, u8).init(allocator);
    var galaxies = std.ArrayList(Point2D).init(allocator);

    var splits = std.mem.split(u8, data, "\n");
    var il: usize = 0;
    while (splits.next()) |line| : (il += 1) {
        //var ic: i32 = 0;
        //var map_lines = std.mem.split(u8, line, "\n");
        for (line, 0..) |l, ic| {
            if (l == '#') {
                //try galaxies.put(Point2D.new(il, ic), 0);
                try galaxies.append(Point2D.new(il, ic));
            }
        }
    }
    std.debug.print("Galaxies size = {}\n", .{galaxies.items.len});
    // for (galaxies.items) |point| {
    //     std.debug.print("{}\n", .{point});
    // }

    var galaxies_p1 = try expand(galaxies, 2);
    std.debug.print("Part 1 (x 2) = {}\n", .{count_shortest_distances(&galaxies_p1)});

    var galaxies_p1_bis = try expand(galaxies, 10);
    std.debug.print("Part 1 (x 10) = {}\n", .{count_shortest_distances(&galaxies_p1_bis)});

    var galaxies_p2 = try expand(galaxies, 1000000);
    std.debug.print("Part 2 (x 1000000) = {}\n", .{count_shortest_distances(&galaxies_p2)});
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 11: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }
    try solve(if (example) fileDataEx else fileData);
}
