import Std

namespace Q335

/-- Subsets of six points are represented by the numbers 0 through 63. -/
abbrev Mask := Fin 64

def family (a : Nat) : Bool := [1, 5, 7, 9, 25, 44, 45, 47, 61].contains a

private def layers : List (List Nat) := [
  [18,22,26,30,50,54,58],
  [10,14,19,20,28,34,38,42,48,51,52,56,62],
  [2,6,16,24,32,35,49,55,59],
  [23,27,33,36,40,43,46,53,60], [11,21,31,39,57],
  [3,12,17,37,41], [4,8], [0,15,29], [13,63], [7,25,44],
  [47,61], [5,9], [1], [45]]

def height (a : Nat) : Nat := layers.findIdx (fun layer => layer.contains a)

set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

theorem corners : ∀ a b : Mask, family a.val = true → family b.val = true →
    family (a.val ||| b.val) = true ∨ family (a.val &&& b.val) = true := by decide

theorem outsideBeforeInside : ∀ a b : Mask, family a.val = false → family b.val = true →
    height a.val < height b.val := by decide

def advances (a b opposite : Nat) : Prop :=
  (family opposite = false ∧ family a = family b) → height a < height b

instance (a b d : Nat) : Decidable (advances a b d) := by unfold advances; infer_instance

theorem cornerArcs : ∀ a c : Mask, family c.val = true →
    advances a.val (a.val ||| c.val) (a.val &&& c.val) ∧
    advances a.val (a.val &&& c.val) (a.val ||| c.val) := by decide

/-- All outside-to-inside arrows, and both possible same-side corner arrows. -/
inductive Arc : Mask → Mask → Prop where
  | outside (a b : Mask) (ha : family a.val = false) (hb : family b.val = true) : Arc a b
  | corner (a b c : Mask) (hc : family c.val = true)
      (side : family a.val = family b.val)
      (cases : (b.val = a.val ||| c.val ∧ family (a.val &&& c.val) = false) ∨
               (b.val = a.val &&& c.val ∧ family (a.val ||| c.val) = false)) : Arc a b

theorem rises {a b : Mask} (h : Arc a b) : height a.val < height b.val := by
  cases h with
  | outside ha hb => exact outsideBeforeInside _ _ ha hb
  | corner c hc hs h =>
    obtain ⟨left, right⟩ := cornerArcs _ c hc
    rcases h with ⟨hb, ho⟩ | ⟨hb, ho⟩
    · rw [hb] at hs ⊢
      exact left ⟨ho, hs⟩
    · rw [hb] at hs ⊢
      exact right ⟨ho, hs⟩

/-- A path here is nonempty, so self-reachability is a directed cycle. -/
inductive Path : Mask → Mask → Prop where
  | edge {a b : Mask} : Arc a b → Path a b
  | extend {a b c : Mask} : Path a b → Arc b c → Path a c

theorem pathIncreases {a b : Mask} (h : Path a b) : height a.val < height b.val := by
  induction h with
  | edge e => exact rises e
  | extend _ e ih => exact Nat.lt_trans ih (rises e)

theorem acyclic (a : Mask) : ¬ Path a a := fun p => (Nat.lt_irrefl _) (pathIncreases p)

theorem maskOperations : ∀ a b : Mask,
    (a ||| b).val = (a.val ||| b.val) ∧ (a &&& b).val = (a.val &&& b.val) := by decide

section
open Lean.Grind
variable {R : Type} [CommRing R] [LE R] [LT R] [Std.IsLinearOrder R]
  [Std.LawfulOrderLT R] [OrderedRing R]

/-- A real-valued submodular strict threshold would instantiate these laws. -/
theorem noThreshold (f : Mask → R) (k : R)
    (submod : ∀ a b : Mask, f (a ||| b) + f (a &&& b) ≤ f a + f b)
    (threshold : ∀ a : Mask, family a.val = true ↔ f a < k) : False := by
  have h₁ : f 31 + f 1 ≤ f 7 + f 25 := submod 7 25
  have h₂ : f 63 + f 12 ≤ f 31 + f 44 := submod 31 44
  have h₃ : f 13 + f 0 ≤ f 12 + f 1 := submod 12 1
  have t₁ : f 7 < k := (threshold 7).mp (by decide)
  have t₂ : f 25 < k := (threshold 25).mp (by decide)
  have t₃ : f 44 < k := (threshold 44).mp (by decide)
  have n₁ : ¬ f 63 < k := fun h => (by decide : ¬ family 63 = true) ((threshold 63).mpr h)
  have n₂ : ¬ f 13 < k := fun h => (by decide : ¬ family 13 = true) ((threshold 13).mpr h)
  have n₃ : ¬ f 0 < k := fun h => (by decide : ¬ family 0 = true) ((threshold 0).mpr h)
  clear submod threshold
  grind

theorem witness :
    (∀ a b : Mask, family a.val = true → family b.val = true →
      family (a.val ||| b.val) = true ∨ family (a.val &&& b.val) = true) ∧
    (∀ a : Mask, ¬ Path a a) ∧
    ¬ ∃ (f : Mask → R) (k : R),
      (∀ a b, f (a ||| b) + f (a &&& b) ≤ f a + f b) ∧
      (∀ a : Mask, family a.val = true ↔ f a < k) := by
  refine ⟨corners, acyclic, ?_⟩
  rintro ⟨f, k, hs, ht⟩
  exact noThreshold f k hs ht
end

#print axioms maskOperations
#print axioms witness
#print axioms corners
#print axioms acyclic
#print axioms noThreshold
end Q335
