#!/usr/bin/env kscript

import java.io.File

// Almost the same as puzzle13.py (Python3)

/**
 * Representation of the firewall in the puzzle.
 */
class Firewall(puzzleInput: String) {

  var ticks = 0 // Current picoseconds
  val rangeByDepth: Map<Int, Int> = puzzleInput.split("\n")
    .map { it.split(": ") }
    .map { Pair(it[0].toInt(), it[1].toInt()) }
    .toMap()
  val maxDepth = rangeByDepth.keys.max() ?: 0

  fun tick() {
    ticks++
  }

  /**
   * Returns the current layer position.
   * If no layer exists, -1 will be returned.
   */
  fun getLayerPosition(depth: Int): Int {
    if(depth !in rangeByDepth.keys)
      return -1

      // Source: https://stackoverflow.com/a/11544567/3949509
      val range = rangeByDepth[depth]!! - 1
      return Math.abs(((ticks + range) % (range * 2)) - range)
  }

}

fun solvePart1(firewall: Firewall): Int {
  var serverity = 0
  for(depth in 0..firewall.maxDepth) {
    if(firewall.getLayerPosition(depth) == 0)
      serverity += depth * firewall.rangeByDepth[depth]!!
    firewall.tick()
  }
  return serverity
}

/**
 * Returns whether you would get caught in the 'firewall'.
 */
fun isCaught(firewall: Firewall): Boolean {
    for(depth in 0..firewall.maxDepth) {
        if(firewall.getLayerPosition(depth) == 0)
            return true
        firewall.tick()
    }
    return false
}

fun solvePart2(firewall: Firewall): Int {
  var ticksDelayed = 0
  while(true) {
    firewall.ticks = ticksDelayed
      if(!isCaught(firewall))
        return ticksDelayed
    ticksDelayed++
  }
}

fun main(args: Array<String>) {
  val puzzleInput = File("../inputs/input13").readText().trim()

  val start = System.currentTimeMillis()  // To measure time

  val firewall = Firewall(puzzleInput)
  println("Solutions:")
  println("Day 13 Part 1: ${solvePart1(firewall)}")
  println("Day 13 Part 2: ${solvePart2(firewall)}")

  println("Duration: ${System.currentTimeMillis() - start} ms")
}
