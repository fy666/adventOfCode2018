const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day18.txt");
const fileDataEx = @embedFile("./files/day18ex.txt");

const Point2D = utils.Point2D;
pub const Plan = struct { direction: u8, steps: i32 };

fn parse_line(data: []const u8, part2: bool) !Plan {
    if (!part2) {
        var split_label = std.mem.splitAny(u8, data, " ()");
        var dir = split_label.first()[0];
        var after = split_label.next();
        var steps = try std.fmt.parseInt(i32, after.?, 10);
        return Plan{ .direction = dir, .steps = steps };
    }
    var split_label = std.mem.splitAny(u8, data, "#");
    _ = split_label.first();
    var after = split_label.next();
    var steps = try std.fmt.parseInt(i32, after.?[0..5], 16);
    var ix = try std.fmt.parseInt(usize, after.?[5..6], 10);
    const dirs: []const u8 = "RDLU";
    return Plan{ .direction = dirs[ix], .steps = steps };
}

fn get_countours(data: anytype, allocator: std.mem.Allocator, part2: bool) !struct { std.ArrayList(Point2D), i32 } {
    var contours = std.ArrayList(Point2D).init(allocator);
    var pos = Point2D.new(0, 0);
    try contours.append(pos);

    var splits = std.mem.split(u8, data, "\n");
    var perimeter: i32 = 0;
    while (splits.next()) |line| {
        var plan = try parse_line(line, part2);
        var delta = switch (plan.direction) {
            'R' => Point2D.new(0, plan.steps),
            'L' => Point2D.new(0, -plan.steps),
            'U' => Point2D.new(-plan.steps, 0),
            'D' => Point2D.new(plan.steps, 0),
            else => unreachable,
        };
        var new_pos = pos.add(&delta);
        if (plan.direction == 'D' or plan.direction == 'L') {
            perimeter += plan.steps;
        }
        try contours.append(new_pos);
        pos = new_pos;
        // parse contour
    }

    return .{ contours, perimeter + 1 };
}

fn compute_contour(data: std.ArrayList(Point2D)) i64 {
    var s: i64 = 0;
    var it = std.mem.window(Point2D, data.items, 2, 1);
    while (it.next()) |slice| {
        //std.debug.print("Slice = {any}\n", .{slice});
        var x: i64 = (slice[0].y + slice[1].y);
        var y: i64 = (slice[0].x - slice[1].x);
        s += x * y;
    }
    s = @divExact(s, 2);
    return @intCast(@abs(s));
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 18: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }

    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    {
        var contours = try get_countours(if (example) fileDataEx else fileData, allocator, false);
        var ans = compute_contour(contours[0]) + contours[1];
        std.debug.print("Part 1 = {}\n", .{ans});
    }
    {
        var contours = try get_countours(if (example) fileDataEx else fileData, allocator, true);
        var ans = compute_contour(contours[0]) + contours[1];
        std.debug.print("Part 2 = {}\n", .{ans});
    }
}
