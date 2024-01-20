const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day23.txt");
const fileDataEx = @embedFile("./files/day23ex.txt");

const Point2D = utils.Point2D;
const Allocator = std.mem.Allocator;

const PointHash = std.AutoHashMap(Point2D, bool);

pub const SearchItem = struct { score: i32, pos: Point2D, prev: PointHash };

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

fn get_map(data: anytype, allocator: Allocator) ![][]const u8 {
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
    return map;
}

fn get_map_tile(map: *const [][]const u8, pos: Point2D) ?u8 {
    var maxX: usize = map.len;
    var maxY: usize = map.*[0].len;
    var x = pos.getX(maxX) catch {
        return null;
    };
    var y = pos.getY(maxY) catch {
        return null;
    };
    return map.*[x][y];
}

fn solve_part1(map: [][]const u8, start_pos: Point2D, end_pos: Point2D, allocator: Allocator) !usize {
    const CustomQueue = std.PriorityQueue(SearchItem, void, comptime cmpFunc);
    var queue = CustomQueue.init(allocator, {});

    var first_search_item = SearchItem{ .score = 0, .pos = start_pos, .prev = PointHash.init(allocator) };
    try queue.add(first_search_item);

    const dirs = utils.get4Directions();
    var max_path: usize = 0;

    while (queue.count() > 0) {
        var item = queue.remove();
        if (utils.customEquality(item.pos, end_pos)) {
            max_path = @max(max_path, item.prev.count());
            //std.debug.print("Max path = {}\n", .{max_path});
            continue;
        }

        var tile = get_map_tile(&map, item.pos);
        if (tile == null) {
            continue;
        }

        for (dirs) |dir| {
            var local_dirs = switch (tile.?) {
                '>' => Point2D{ .x = 0, .y = 1 },
                '^' => Point2D{ .x = -1, .y = 0 },
                'v' => Point2D{ .x = 1, .y = 0 },
                '<' => Point2D{ .x = 0, .y = -1 },
                else => null,
            };
            if (local_dirs != null and !std.meta.eql(local_dirs.?, dir)) {
                continue;
            }
            var new_position = item.pos.add(&dir);
            var new_tile = get_map_tile(&map, item.pos);
            if (new_tile == null or new_tile.? == '#') {
                continue;
            }
            if (item.prev.contains(new_position)) {
                continue;
            }

            var new_search_item = SearchItem{ .score = item.score - 1, .pos = new_position, .prev = try item.prev.clone() };
            try new_search_item.prev.put(new_position, false);
            try queue.add(new_search_item);
        }
    }
    return max_path;
}

fn solve_part2(map: [][]const u8, start_pos: Point2D, end_pos: Point2D, allocator: Allocator) !usize {
    // const CustomQueue = std.PriorityQueue(SearchItem, void, comptime cmpFunc);
    // var queue = CustomQueue.init(allocator, {});

    // var first_search_item = SearchItem{ .score = 0, .pos = start_pos, .prev = PointHash.init(allocator) };
    // try queue.add(first_search_item);
    const dirs = utils.get4Directions();
    var max_path: usize = 0;

    const HashOfPoints = std.AutoHashMap(Point2D, i32);
    const PointHashOfHash = std.AutoHashMap(Point2D, HashOfPoints);
    var graph = PointHashOfHash.init(allocator);
    for (map, 0..) |line, x| {
        for (line, 0..) |col, y| {
            if (col == '#') {
                continue;
            }
            var pos = Point2D.new(x, y);
            for (dirs) |dir| {
                var new_position = pos.add(&dir);
                var new_tile = get_map_tile(&map, new_position);
                if (new_tile == null or new_tile.? == '#') {
                    continue;
                }
                var it = try graph.getOrPut(pos);
                if (it.found_existing == false) {
                    it.value_ptr.* = HashOfPoints.init(allocator);
                }
                try it.value_ptr.put(new_position, 1);
                //graph.put(new_position, HashOfPoints.init(allocator));
            }
        }
    }

    {
        var it = graph.iterator();
        while (it.next()) |item| {
            if (item.value_ptr.count() == 2) {
                var it2 = item.value_ptr.iterator();
                var in = it2.next().?;
                var out = it2.next().?;

                var in_out_val: i32 = out.value_ptr.* + graph.getPtr(in.key_ptr.*).?.getPtr(item.key_ptr.*).?.*;
                try graph.getPtr(in.key_ptr.*).?.put(out.key_ptr.*, in_out_val);

                var out_in_val: i32 = in.value_ptr.* + graph.getPtr(out.key_ptr.*).?.getPtr(item.key_ptr.*).?.*;
                try graph.getPtr(out.key_ptr.*).?.put(in.key_ptr.*, out_in_val);

                _ = graph.getPtr(out.key_ptr.*).?.remove(item.key_ptr.*);
                _ = graph.getPtr(in.key_ptr.*).?.remove(item.key_ptr.*);
            }
        }
    }
    // {
    //     var it = graph.iterator();
    //     while (it.next()) |item| {
    //         std.debug.print("[{},{}]:", .{ item.key_ptr.x, item.key_ptr.y });
    //         var it2 = item.value_ptr.iterator();
    //         while (it2.next()) |item2| {
    //             std.debug.print("([{},{}],{}),", .{ item2.key_ptr.x, item2.key_ptr.y, item2.value_ptr.* });
    //         }
    //         std.debug.print("\n", .{});
    //     }
    // }

    var queue = std.ArrayList(SearchItem).init(allocator);

    var first_search_item = SearchItem{ .score = 0, .pos = start_pos, .prev = PointHash.init(allocator) };
    try queue.append(first_search_item);

    while (queue.items.len > 0) {
        var item = queue.pop();
        if (utils.customEquality(item.pos, end_pos)) {
            max_path = @max(max_path, @as(u32, @intCast(item.score)));
            continue;
        }
        var item_childs_it = graph.getPtr(item.pos).?.iterator();
        while (item_childs_it.next()) |child| {
            if (item.prev.contains(child.key_ptr.*)) {
                continue;
            }

            var new_search_item = SearchItem{ .score = item.score + child.value_ptr.*, .pos = child.key_ptr.*, .prev = try item.prev.clone() };
            try new_search_item.prev.put(child.key_ptr.*, false);
            try queue.append(new_search_item);
        }
    }
    return max_path;
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 23: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }

    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var map = try get_map(if (example) fileDataEx else fileData, allocator);

    // Find start and end position
    var maxX: usize = map.len;
    var maxY: usize = map[0].len;
    std.debug.print("Find map of {} x {} \n", .{ maxX, maxY });
    var start_pos = Point2D.new(0, 1);
    var end_pos = Point2D.new(maxX - 1, maxY - 2);
    std.debug.print("Start at ({},{}), end at ({},{}) \n", .{ start_pos.x, start_pos.y, end_pos.x, end_pos.y });

    var timer = try std.time.Timer.start();
    var part1 = try solve_part1(map, start_pos, end_pos, allocator);
    var ts: f32 = @as(f32, @floatFromInt(timer.lap()));
    std.debug.print("Part 1 = {} (in {} s, {} ms)\n", .{ part1, ts / 1e9, ts / 1e6 });

    timer.reset();
    var part2 = try solve_part2(map, start_pos, end_pos, allocator);
    ts = @as(f32, @floatFromInt(timer.lap()));
    std.debug.print("Part 2 = {} (in {} s, {} ms)\n", .{ part2, ts / 1e9, ts / 1e6 });
}
