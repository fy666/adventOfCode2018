const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day17.txt");
const fileDataEx = @embedFile("./files/day17ex.txt");
const fileDataEx2 = @embedFile("./files/day17ex2.txt");

const Point2D = utils.Point2D;
const arrayType = std.ArrayListAligned(Point2D, null);

pub const SearchItem = struct { score: i32, pos: Point2D, last_direction: ?Point2D, last_direction_counter: i32, positions: arrayType };

// should return true if a < b :)
fn cmpFunc(context: void, a: SearchItem, b: SearchItem) std.math.Order {
    _ = context;
    if (a.score == b.score) {
        return std.math.Order.eq;
    } else if (a.score > b.score) {
        return std.math.Order.gt;
    } else if (a.score < b.score) {
        return std.math.Order.lt;
    }
    unreachable;
}

fn is_valid_dir_new(last_direction: ?Point2D, counter: i32, new_dir: Point2D, part2: bool) bool {
    if (last_direction == null) {
        return true;
    }

    if (last_direction.?.x == -new_dir.x and last_direction.?.y == -new_dir.y) {
        return false; // Cannot go back
    }
    // PART2 CHANGE
    if (part2) {
        if (!utils.customEquality(last_direction.?, new_dir) and counter < 4) {
            return false;
        }

        if (utils.customEquality(last_direction.?, new_dir) and counter == 10) {
            return false;
        }
    } else {
        if (utils.customEquality(last_direction.?, new_dir) and counter == 3) {
            return false;
        }
    }
    return true;
}

fn solve(data: anytype, part2: bool) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var len: usize = 0;
    var splitsLines = std.mem.split(u8, data, "\n");
    while (splitsLines.next()) |_| {
        len += 1;
    }

    var map: [][]const u8 = undefined;
    map = try allocator.alloc([]const u8, len);
    var splits = std.mem.split(u8, data, "\n");
    for (map, 0..) |_, i| {
        map[i] = splits.next() orelse unreachable;
    }
    // Find start position
    var maxX: usize = len;
    var maxY: usize = map[0].len;
    std.debug.print("Find lava map of {} x {} \n", .{ maxX, maxY });
    var combi_hash = std.StringHashMap(i32).init(allocator);
    defer combi_hash.deinit();
    const CustomQueue = std.PriorityQueue(SearchItem, void, comptime cmpFunc);
    var queue = CustomQueue.init(allocator, {});
    var startPos = Point2D.new(0, 0);
    var endPos = Point2D.new(maxX - 1, maxY - 1);

    var current_search_item = SearchItem{ .score = 0, .pos = startPos, .last_direction = null, .last_direction_counter = 0, .positions = std.ArrayList(Point2D).init(allocator) };

    const dirs = utils.get4Directions();
    var ix: i32 = 0;
    while (true) : (ix += 1) {
        if (utils.customEquality(current_search_item.pos, endPos) and (!part2 or current_search_item.last_direction_counter >= 4)) {
            break;
        }
        for (dirs) |dir| {
            var new_item = current_search_item; // hopes it copies
            var position = current_search_item.pos.add(&dir);
            // if dir not already visited
            if (!is_valid_dir_new(current_search_item.last_direction, current_search_item.last_direction_counter, dir, part2)) {
                continue;
            }

            var x = position.getX(maxX) catch {
                continue;
            };
            var y = position.getY(maxY) catch {
                continue;
            };
            var score: i32 = @intCast(map[x][y] - '0'); // - 48
            new_item.pos = position;
            new_item.score += score;
            if (new_item.last_direction == null or !utils.customEquality(new_item.last_direction.?, dir)) {
                new_item.last_direction = dir;
                new_item.last_direction_counter = 1;
            } else {
                new_item.last_direction_counter += 1;
            }

            new_item.positions = try new_item.positions.clone();
            try new_item.positions.append(new_item.pos);

            const hash_of_item = try std.fmt.allocPrint(allocator, "{},{},{},{},{}", .{ new_item.pos.x, new_item.pos.y, new_item.last_direction.?.x, new_item.last_direction.?.y, new_item.last_direction_counter });

            if (combi_hash.contains(hash_of_item) == true) {
                continue;
            }
            try queue.add(new_item);
            try combi_hash.put(hash_of_item, new_item.score);
        }
        current_search_item = queue.remove();
    }

    std.debug.print("{s}: score {}\n", .{ if (part2) "Part 2" else "Part 1", current_search_item.score });

    // std.debug.print("Positions = ", .{});
    // for (current_search_item.positions.items) |pos| {
    //     std.debug.print("({},{})", .{ pos.x, pos.y });
    // }
    // std.debug.print("\n", .{});
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 17: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }

    try solve(if (example) fileDataEx else fileData, false);
    try solve(if (example) fileDataEx else fileData, true);

    if (example) {
        //try solve(fileDataEx2, false);
        std.debug.print("Other example:\n", .{});
        try solve(fileDataEx2, true);
    }
}

test "valid_dir_new" {
    var previous_pos: ?Point2D = Point2D{ .x = 0, .y = 1 };
    var newDir = Point2D{ .x = 0, .y = 1 };
    var res = is_valid_dir_new(previous_pos, 2, newDir, false);
    //td.debug.print("{any} and {any} -> {}\n", .{ previous_pos, newDir, res });
    try std.testing.expect(res == true);

    res = is_valid_dir_new(previous_pos, 3, newDir, false);
    try std.testing.expect(res == false);

    res = is_valid_dir_new(null, 0, newDir, false);
    try std.testing.expect(res == true);

    previous_pos = Point2D{ .x = 0, .y = -1 };
    res = is_valid_dir_new(previous_pos, 1, newDir, false);
    try std.testing.expect(res == false);
}
