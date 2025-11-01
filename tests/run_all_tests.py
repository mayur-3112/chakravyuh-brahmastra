"""
Brahmastra Test Suite Dashboard
Comprehensive test runner with beautiful output
Save as: ~/chakravyuh/brahmastra/tests/run_all_tests.py
"""

import unittest
import sys
import time
from io import StringIO
from datetime import datetime

class ColoredTextTestResult(unittest.TextTestResult):
    """Custom test result with colored output"""
    
    # ANSI color codes
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_times = {}
        self.start_time = None
    
    def startTest(self, test):
        super().startTest(test)
        self.start_time = time.time()
        test_name = self.getDescription(test)
        print(f"{self.CYAN}→ Running: {test_name}{self.RESET}")
    
    def addSuccess(self, test):
        super().addSuccess(test)
        duration = time.time() - self.start_time
        self.test_times[test] = duration
        test_name = self.getDescription(test)
        print(f"{self.GREEN}✓ PASSED: {test_name} ({duration:.3f}s){self.RESET}")
    
    def addError(self, test, err):
        super().addError(test, err)
        test_name = self.getDescription(test)
        print(f"{self.RED}✗ ERROR: {test_name}{self.RESET}")
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        test_name = self.getDescription(test)
        print(f"{self.RED}✗ FAILED: {test_name}{self.RESET}")
    
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        test_name = self.getDescription(test)
        print(f"{self.YELLOW}⊘ SKIPPED: {test_name} - {reason}{self.RESET}")


class BrahmastraTestRunner:
    """Custom test runner with dashboard output"""
    
    def __init__(self):
        self.start_time = None
        self.total_duration = 0
    
    def print_header(self):
        """Print dashboard header"""
        print("\n" + "="*80)
        print("█▀▀▄ █▀▀█ █▀▀█ █  █ █▀▄▀█ █▀▀█ █▀▀ ▀▀█▀▀ █▀▀█ █▀▀█")
        print("█▀▀▄ █▄▄▀ █▄▄█ █▀▀█ █ ▀ █ █▄▄█ ▀▀█   █   █▄▄▀ █▄▄█")
        print("▀▀▀  ▀ ▀▀ ▀  ▀ ▀  ▀ ▀   ▀ ▀  ▀ ▀▀▀   ▀   ▀ ▀▀ ▀  ▀")
        print("                  COMPREHENSIVE TEST SUITE")
        print("="*80)
        print(f"Project Chakravyuh | Sir MVIT Bangalore")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80 + "\n")
    
    def print_section(self, title):
        """Print section separator"""
        print(f"\n{'─'*80}")
        print(f"📦 {title}")
        print(f"{'─'*80}\n")
    
    def run_test_suite(self, test_suite, suite_name):
        """Run a test suite and return results"""
        print(f"\n{'='*80}")
        print(f"🧪 {suite_name}")
        print(f"{'='*80}\n")
        
        runner = unittest.TextTestRunner(
            resultclass=ColoredTextTestResult,
            verbosity=2,
            stream=sys.stdout
        )
        
        result = runner.run(test_suite)
        return result
    
    def print_summary(self, all_results):
        """Print comprehensive test summary"""
        total_run = sum(r.testsRun for r in all_results)
        total_failures = sum(len(r.failures) for r in all_results)
        total_errors = sum(len(r.errors) for r in all_results)
        total_skipped = sum(len(r.skipped) for r in all_results)
        total_success = total_run - total_failures - total_errors - total_skipped
        
        print("\n" + "="*80)
        print("📊 TEST SUITE SUMMARY")
        print("="*80)
        
        # Overall statistics
        print(f"\n{'Test Category':<30} {'Count':>10} {'Status':>20}")
        print("-"*80)
        print(f"{'Total Tests Run':<30} {total_run:>10} {'':>20}")
        
        if total_success > 0:
            print(f"{'✓ Passed':<30} {total_success:>10} {self._get_color('GREEN')}{'EXCELLENT':>20}{self._get_color('RESET')}")
        
        if total_failures > 0:
            print(f"{'✗ Failed':<30} {total_failures:>10} {self._get_color('RED')}{'NEEDS FIX':>20}{self._get_color('RESET')}")
        
        if total_errors > 0:
            print(f"{'✗ Errors':<30} {total_errors:>10} {self._get_color('RED')}{'CRITICAL':>20}{self._get_color('RESET')}")
        
        if total_skipped > 0:
            print(f"{'⊘ Skipped':<30} {total_skipped:>10} {self._get_color('YELLOW')}{'INFO':>20}{self._get_color('RESET')}")
        
        print("-"*80)
        
        # Success rate
        if total_run > 0:
            success_rate = (total_success / total_run) * 100
            print(f"\n{'Success Rate:':<30} {success_rate:>6.2f}%")
        
        # Duration
        print(f"{'Total Duration:':<30} {self.total_duration:>10.3f}s")
        
        # Overall status
        print("\n" + "="*80)
        if total_failures == 0 and total_errors == 0:
            print(f"{self._get_color('GREEN')}{self._get_color('BOLD')}")
            print("✅ ALL TESTS PASSED - PRODUCTION READY! 🚀")
            print(f"{self._get_color('RESET')}")
        else:
            print(f"{self._get_color('RED')}{self._get_color('BOLD')}")
            print("❌ SOME TESTS FAILED - REVIEW REQUIRED")
            print(f"{self._get_color('RESET')}")
        print("="*80 + "\n")
    
    def _get_color(self, color_name):
        """Get ANSI color code"""
        colors = {
            'GREEN': '\033[92m',
            'RED': '\033[91m',
            'YELLOW': '\033[93m',
            'BLUE': '\033[94m',
            'CYAN': '\033[96m',
            'BOLD': '\033[1m',
            'RESET': '\033[0m'
        }
        return colors.get(color_name, '')
    
    def run_all_tests(self):
        """Run all test suites"""
        self.print_header()
        self.start_time = time.time()
        
        all_results = []
        
        # Test Suite 1: Models
        self.print_section("TEST SUITE 1: DATA MODELS")
        from tests import test_models
        models_suite = unittest.TestLoader().loadTestsFromModule(test_models)
        models_result = self.run_test_suite(models_suite, "Models & Data Structures")
        all_results.append(models_result)
        
        # Test Suite 2: Engine Units
        self.print_section("TEST SUITE 2: ENGINE COMPONENTS")
        from tests import test_engine_unit
        engine_suite = unittest.TestLoader().loadTestsFromModule(test_engine_unit)
        engine_result = self.run_test_suite(engine_suite, "Engine Unit Tests")
        all_results.append(engine_result)
        
        # Calculate total duration
        self.total_duration = time.time() - self.start_time
        
        # Print comprehensive summary
        self.print_summary(all_results)
        
        # Return exit code
        total_failures = sum(len(r.failures) for r in all_results)
        total_errors = sum(len(r.errors) for r in all_results)
        
        return 0 if (total_failures == 0 and total_errors == 0) else 1


if __name__ == '__main__':
    runner = BrahmastraTestRunner()
    exit_code = runner.run_all_tests()
    sys.exit(exit_code)
