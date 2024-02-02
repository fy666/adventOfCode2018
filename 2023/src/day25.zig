const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day25.txt");
const fileDataEx = @embedFile("./files/day25ex.txt");

const Regex = @import("zig-regex").Regex;

const Allocator = std.mem.Allocator;

const stuple = struct {
    first: []const u8,
    second: []const u8,

    pub fn eql(self: stuple, other: stuple) bool {
        if ((std.mem.eql(u8, self.first, other.first) and std.mem.eql(u8, self.second, other.second)) or (std.mem.eql(u8, self.first, other.second) and std.mem.eql(u8, self.second, other.first))) {
            return true;
        }
        return false;
    }
};

fn valid_connexion(node: stuple, cut_connexions: std.ArrayList(stuple)) bool {
    for (cut_connexions.items) |item| {
        if (node.eql(item)) {
            return false;
        }
    }
    return true;
}

fn walkthrough(tree: *std.StringHashMap(std.ArrayList([]const u8)), allocator: Allocator, node: []const u8, cut_connexions: std.ArrayList(stuple)) !usize {
    var visited_nodes = std.StringHashMap(bool).init(allocator);
    var nodes_to_visit = std.ArrayList([]const u8).init(allocator);
    try nodes_to_visit.append(node);
    while (nodes_to_visit.items.len > 0) {
        var current = nodes_to_visit.orderedRemove(0);
        try visited_nodes.put(current, false);
        for (tree.get(current).?.items) |child| {
            var s = stuple{ .first = child, .second = current };
            if (!visited_nodes.contains(child) and valid_connexion(s, cut_connexions)) {
                try nodes_to_visit.append(child);
            }
        }
    }
    return visited_nodes.count();
}

fn parse_tree_entry(
    line: []const u8,
    allocator: Allocator,
    tree: *std.StringHashMap(std.ArrayList([]const u8)),
) !void {
    var re = try Regex.compile(allocator, "(\\w+): (.*)");
    var captures = try re.captures(line);
    if (captures != null) {
        var node = captures.?.sliceAt(1).?;

        var splitsLines = std.mem.split(u8, captures.?.sliceAt(2).?, " ");
        var childs = std.ArrayList([]const u8).init(allocator);

        while (splitsLines.next()) |item| {
            try childs.append(item);
        }
        try tree.put(node, childs);
    } else {
        std.debug.print("{s} not found\n", .{line});
        unreachable;
    }
}

fn solve(data: anytype, example: bool) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();

    var splitsLines = std.mem.split(u8, data, "\n");

    var tree = std.StringHashMap(std.ArrayList([]const u8)).init(allocator);

    while (splitsLines.next()) |l| {
        try parse_tree_entry(l, allocator, &tree);
    }

    // Bi-directionnal fill
    var it = tree.iterator();
    while (it.next()) |item| {
        var childs = item.value_ptr.*;
        for (childs.items) |child| {
            //std.debug.print("Adding {s} to {s}\n", .{ item.key_ptr.*, child });
            var other_node: ?*std.ArrayList([]const u8) = tree.getPtr(child);
            if (other_node != null) {
                try other_node.?.append(item.key_ptr.*);
            } else {
                // std.debug.print("Null node\n", .{});
                var node_childs = std.ArrayList([]const u8).init(allocator);
                try node_childs.append(item.key_ptr.*);
                try tree.put(child, node_childs);
            }
        }
    }

    // print tree
    // it = tree.iterator();
    // while (it.next()) |item| {
    //     std.debug.print("{s} ->", .{item.key_ptr.*});
    //     var childs = item.value_ptr.*;
    //     for (childs.items) |child| {
    //         std.debug.print("{s},", .{child});
    //     }
    //     std.debug.print("\n", .{});
    // }

    std.debug.print("Size of tree = {} \n", .{tree.count()});

    var cut_connexions = std.ArrayList(stuple).init(allocator);
    if (example) {
        try cut_connexions.append(stuple{ .first = "hfx", .second = "pzl" });
        try cut_connexions.append(stuple{ .first = "bvb", .second = "cmg" });
        try cut_connexions.append(stuple{ .first = "nvd", .second = "jqt" });
    } else {
        try cut_connexions.append(stuple{ .first = "kkp", .second = "vtv" });
        try cut_connexions.append(stuple{ .first = "cmj", .second = "qhd" });
        try cut_connexions.append(stuple{ .first = "lnf", .second = "jll" });
    }

    it = tree.iterator();
    var sizes_map = std.AutoHashMap(usize, usize).init(allocator);
    while (it.next()) |item| {
        var res = try walkthrough(&tree, allocator, item.key_ptr.*, cut_connexions);
        if (!sizes_map.contains(res)) {
            try sizes_map.put(res, res);
        }
        if (sizes_map.count() == 2) {
            break;
        }
    }
    var part1_res: usize = 1;
    var itm = sizes_map.valueIterator();
    while (itm.next()) |l| {
        part1_res *= l.*;
    }
    std.debug.print("Walkthrough of = {} \n", .{part1_res});
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 25: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }

    try solve(if (example) fileDataEx else fileData, example);
}
