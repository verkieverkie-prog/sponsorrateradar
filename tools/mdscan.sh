cd "$(dirname "$0")/../content/guides"
echo tables; grep -h "^|" *.md | head -4
echo counts; grep -c "^|" *.md
echo blocks; grep -h -E '^([0-9]+\. |> |```|\* |- |---$)' *.md | cut -c1-3 | sort | uniq -c
echo inline; grep -ho -E '`[^`]+`|_[a-z]+_|\*[^* ][^*]*\*' *.md | head
