use std::cmp::Ordering;
use std::collections::BTreeMap;
use std::ops::{Add, Sub};
use std::str::FromStr;

pub trait MinPositive<T> {
    const MIN_POSITIVE: T;
}
impl MinPositive<f64> for f64 {
    const MIN_POSITIVE: f64 = f64::MIN_POSITIVE;
}

impl MinPositive<f32> for f32 {
    const MIN_POSITIVE: f32 = f32::MIN_POSITIVE;
}

impl MinPositive<i32> for i32 {
    const MIN_POSITIVE: i32 = 1;
}

impl MinPositive<i64> for i64 {
    const MIN_POSITIVE: i64 = 1;
}

impl MinPositive<i128> for i128 {
    const MIN_POSITIVE: i128 = 1;
}

impl MinPositive<u32> for u32 {
    const MIN_POSITIVE: u32 = 1;
}

impl MinPositive<u64> for u64 {
    const MIN_POSITIVE: u64 = 1;
}

impl MinPositive<u128> for u128 {
    const MIN_POSITIVE: u128 = 1;
}

#[derive(Debug, PartialEq, PartialOrd, Copy, Clone)]
pub struct OrderedFloat<T>(T);

impl<T: PartialEq> Eq for OrderedFloat<T> {}

impl<T: PartialOrd> Ord for OrderedFloat<T> {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap_or(Ordering::Equal)
    }
}

pub fn parse_interval<T>(
    interval: &str,
) -> Result<(OrderedFloat<T>, OrderedFloat<T>, bool, bool), &'static str>
where
    T: FromStr + PartialOrd + Copy,
{
    let inclusive_start = interval.starts_with('[');
    let inclusive_end = interval.ends_with(']');
    let interval = interval.trim_matches(|c| c == '[' || c == ']' || c == '(' || c == ')');
    let nums: Vec<T> = interval
        .split(',')
        .map(|s| s.trim().parse().map_err(|_| "Invalid number format"))
        .collect::<Result<Vec<T>, _>>()?;

    if nums.len() != 2 {
        return Err("Invalid interval format");
    }

    Ok((
        OrderedFloat(nums[0]),
        OrderedFloat(nums[1]),
        inclusive_start,
        inclusive_end,
    ))
}

pub fn make_interval_match<T>(intervals: &str) -> impl Fn(T) -> String
where
    T: MinPositive<T>
        + PartialOrd
        + Copy
        + std::fmt::Display
        + FromStr
        + Add<Output = T>
        + Sub<Output = T>,
{
    let interval_list: Vec<&str> = intervals.split(';').map(|s| s.trim()).collect();
    let mut interval_map: BTreeMap<(OrderedFloat<T>, OrderedFloat<T>), (bool, bool, String)> =
        BTreeMap::new();

    for interval in interval_list {
        if let Ok((lower, upper, incl_start, incl_end)) = parse_interval(interval) {
            interval_map.insert((lower, upper), (incl_start, incl_end, interval.to_string()));
        }
    }

    move |n: T| -> String {
        for (&(lower, upper), &(incl_start, incl_end, ref interval_str)) in interval_map.range(..) {
            let lower_bound = if incl_start {
                lower.0
            } else {
                lower.0 + T::MIN_POSITIVE
            };
            let upper_bound = if incl_end {
                upper.0
            } else {
                upper.0 - T::MIN_POSITIVE
            };

            if (lower_bound..=upper_bound).contains(&n) {
                return interval_str.clone();
            }
        }
        "None".to_string()
    }
}
