#!/usr/bin/env kscript

import java.io.File

val puzzleInput = File("../inputs/input1").readText().trim()
val size = puzzleInput.length

val secondIndexMapperPart1 = { index: Int -> (index + 1) % size }
val secondIndexMapperPart2 = { index: Int -> (size / 2 + index) % size }

fun solvePuzzle(secondIndexMapper: (Int) -> Int): Int {
  val digits = puzzleInput.toCharArray().map { it.toString().toInt() }
  return (0 until digits.size)
    .map { Pair(it, secondIndexMapper(it)) }
    .map { Pair(digits[it.first], digits[it.second]) }
    .filter { it.first == it.second }
    .sumBy { it.first }
}

fun main(args: Array<String>) {
  println("Solutions:")
  println("Day 1 Part 1: ${solvePuzzle(secondIndexMapperPart1)}")
  println("Day 1 Part 2: ${solvePuzzle(secondIndexMapperPart2)}")
}
