from app.calculations import add, BankAccount
import pytest

@pytest.fixture
def initialize_bank_account():
		return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [(20, 10, 30), (50, 60, 110)])

def test_add(num1, num2, expected):
    assert add(num1, num2) ==expected

## before fixture, instantiation is needed
def test_bank_initial_amount():
    bank_account = BankAccount(50)
    assert bank_account.balance==50

##after fixture, notice we do not instantiate the class here
def test_bank_initial_amount(initialize_bank_account):
	assert initialize_bank_account.balance == 50

def test_bank_deposit_amount():
    bank_account = BankAccount(50)
    bank_account.deposit(10)
    assert bank_account.balance==60

def test_bank_withdraw_amount():
    bank_account = BankAccount(50)
    bank_account.withdraw(10)
    assert bank_account.balance==40

def test_bank_interest_amount():
    bank_account = BankAccount(10)
    bank_account.interest(10)
    assert bank_account.balance==11


def test_bank_transaction(initialize_bank_account):
##    bank_account = BankAccount(10)
    initialize_bank_account.deposit(200)
    initialize_bank_account.withdraw(10)
    assert initialize_bank_account.balance==240

##now let's try the transaction using parameterization.
@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 10, 240), (100, 10, 140)]
    )

def test_bank_transaction(initialize_bank_account, deposited, withdrew, expected):
##    bank_account = BankAccount(10)
    initialize_bank_account.deposit(deposited)
    initialize_bank_account.withdraw(withdrew)
    assert initialize_bank_account.balance==expected