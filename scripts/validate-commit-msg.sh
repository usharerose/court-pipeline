#!/bin/bash

# Commit Message Validation Script
# Validates commit messages according to the convention defined in CLAUDE.md

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print functions
print_error() {
    echo -e "${RED}Error: $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}Warning: $1${NC}" >&2
}

# Usage information
usage() {
    echo "Usage: $0 [commit_message_file]"
    echo "  If no file is provided, reads from stdin"
    exit 1
}

# Read commit message
read_commit_message() {
    local msg_file="$1"

    if [ -n "$msg_file" ]; then
        if [ ! -f "$msg_file" ]; then
            print_error "Commit message file not found: $msg_file"
            exit 1
        fi
        message=$(cat "$msg_file")
    else
        message=$(cat)
    fi

    # Remove leading/trailing whitespace
    message=$(echo "$message" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
}

# Validate basic structure
validate_basic_structure() {
    if [ -z "$message" ]; then
        print_error "Commit message cannot be empty"
        return 1
    fi

    # Get header (first line)
    header=$(echo "$message" | head -n 1)

    # Check header length (max 100 chars)
    if [ ${#header} -gt 100 ]; then
        print_error "Header exceeds 100 characters (${#header} chars)"
        return 1
    fi

    return 0
}

# Validate type and scope
validate_type_scope() {
    # Define allowed types (lowercase)
    local allowed_types="build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test"

    # Check format: type(scope): subject or type: subject
    if ! echo "$header" | grep -E "^($allowed_types)(\([^)]+\))?: .+$" > /dev/null; then
        print_error "Commit message must follow format: type(scope): subject or type: subject"
        print_error "Allowed types: build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test"
        print_error "Examples:"
        print_error "  fix: resolve authentication issue"
        print_error "  feat(auth): add two-factor authentication"
        return 1
    fi

    # Extract type and check if it's lowercase
    type=$(echo "$header" | sed -E 's/^([^(:]+).*$/\1/')
    if [ "$type" != "$(echo "$type" | tr '[:upper:]' '[:lower:]')" ]; then
        print_error "Type must be lowercase (found: $type)"
        return 1
    fi

    # Extract and validate scope if present
    if echo "$header" | grep -E '^[^(:]+\([^)]*\):' > /dev/null; then
        scope=$(echo "$header" | sed -E 's/^[^(]+\(([^)]*)\).*$/\1/')

        # Check if scope is empty
        if [ -z "$scope" ]; then
            print_error "Scope cannot be empty when parentheses are used"
            return 1
        fi

        # Check scope format (should be noun-like, no spaces)
        if echo "$scope" | grep -E '[$&;|<>]' > /dev/null; then
            print_error "Scope contains invalid characters: $scope"
            return 1
        fi

        # Warn about scope format (should be noun-like)
        if [ ${#scope} -gt 20 ]; then
            print_warning "Scope is quite long (${#scope} chars), consider shortening it"
        fi
    fi

    return 0
}

# Validate subject
validate_subject() {
    # Extract subject (everything after the colon and space)
    subject=$(echo "$header" | sed -E 's/^[^:]*: //')

    # Check if subject is empty
    if [ -z "$subject" ]; then
        print_error "Subject cannot be empty"
        return 1
    fi

    # Check if subject ends with period
    if echo "$subject" | grep -E '\.$' > /dev/null; then
        print_error "Subject should not end with a period"
        return 1
    fi

    # Check if subject starts with lowercase letter
    first_char=$(echo "$subject" | cut -c1)
    if [ "$first_char" != "$(echo "$first_char" | tr '[:upper:]' '[:lower:]')" ]; then
        print_error "Subject should start with lowercase letter"
        return 1
    fi

    return 0
}

# Validate body structure
validate_body() {
    # Split message into lines
    local lines
    mapfile -t lines <<< "$message"

    # Check if there's a body (more than header)
    if [ ${#lines[@]} -gt 1 ]; then
        # Check for blank line after header
        second_line="${lines[1]}"
        if [ -n "$second_line" ]; then
            print_warning "Body should be separated from header with a blank line"
            return 1  # This is a warning, but we can choose to allow it
        fi

        # Validate body line lengths
        local in_body=false
        local in_footer=false
        local found_blank=false

        for i in "${!lines[@]}"; do
            local line="${lines[$i]}"
            local line_num=$((i + 1))

            # Skip header and blank lines
            if [ $i -eq 0 ]; then
                continue
            fi

            # Mark if we found a blank line
            if [ -z "$line" ]; then
                found_blank=true
                continue
            fi

            # Check line length
            if [ ${#line} -gt 100 ]; then
                print_error "Line $line_num exceeds 100 characters (${#line} chars): ${line:0:50}..."
                return 1
            fi

            # Check for footer indicators (like BREAKING CHANGE)
            if echo "$line" | grep -E '^(BREAKING CHANGE|Deprecate|Remove):' > /dev/null; then
                if [ "$found_blank" = false ] && [ $i -gt 1 ]; then
                    print_warning "Footer should be separated from body with a blank line"
                fi
            fi
        done
    fi

    return 0
}

# Validate footer format
validate_footer() {
    # Check for BREAKING CHANGE format
    if echo "$message" | grep -E "BREAKING CHANGE:" > /dev/null; then
        # Ensure BREAKING CHANGE has proper format (with space after colon)
        if ! echo "$message" | grep -E "BREAKING CHANGE: " > /dev/null; then
            print_error "BREAKING CHANGE must be followed by a space"
            return 1
        fi
    fi

    # Check for proper issue reference formats
    if echo "$message" | grep -E "(Closes|Fixes|Resolves) #[0-9]+" > /dev/null; then
        # Valid formats - no action needed
        return 0
    elif echo "$message" | grep -E "(Closes|Fixes|Resolves)#" > /dev/null; then
        print_error "Issue references must have space after Closes/Fixes/Resolves (e.g., 'Closes #123')"
        return 1
    fi

    return 0
}

# Validate overall format
validate_format() {
    # Check for common format issues
    if echo "$message" | grep -E '^\s*\w+\s*\([^)]*\)\s*:\s*$' > /dev/null; then
        print_error "Commit message has empty subject after colon"
        return 1
    fi

    # Check for multiple consecutive colons
    if echo "$header" | grep -E "::" > /dev/null; then
        print_error "Only one colon allowed after type/scope"
        return 1
    fi

    return 0
}

# Main validation function
validate_commit_message() {
    local msg_file="$1"

    read_commit_message "$msg_file"

    if ! validate_basic_structure; then
        return 1
    fi

    if ! validate_type_scope; then
        return 1
    fi

    if ! validate_subject; then
        return 1
    fi

    if ! validate_body; then
        return 1
    fi

    if ! validate_footer; then
        return 1
    fi

    if ! validate_format; then
        return 1
    fi

    print_success "Commit message is valid!"
    return 0
}

# Script entry point
main() {
    local msg_file="$1"

    # Check for help flag
    if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        usage
    fi

    # Validate the commit message
    if validate_commit_message "$msg_file"; then
        exit 0
    else
        exit 1
    fi
}

# Run main function with all arguments
main "$@"
