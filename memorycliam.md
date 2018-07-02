# ram cliam in eos
## memory claim: the code
When eos smart contract is well-coded, ram can be reclaimed to reduce resource comsumption.  
A well-coded contract removes certain items in database to reclaim memory usage, a good example is in eosio.token:  
```
void token::sub_balance( account_name owner, asset value ) {
   accounts from_acnts( _self, owner );

   const auto& from = from_acnts.get( value.symbol.name(), "no balance object found" );
   eosio_assert( from.balance.amount >= value.amount, "overdrawn balance" );


   if( from.balance.amount == value.amount ) {
      from_acnts.erase( from ); // ram is reclaimd here
   } else {
      from_acnts.modify( from, owner, [&]( auto& a ) {
          a.balance -= value;
      });
   }
}
```
When the amount of the ```from_acnts``` becomes zero, his items is erased from database, so the memory reclaimed.


## memory claim: an experiment
In ```testcliam.py```(if you want to run it, please modify wallet password and account public key), we check memory usage of the following steps:  
1、create the contract account,   
2、the issue a token,   
3、issue 1000 tokens to 1000 clients,  
4、transfer 1000 clients's token back to contract account  

After running the script:
```
python claim.py &>> claim.txt
```

In ```cliam.txt``` we can see memory usage log:
```
after set contract code, memory usage is: 192810
after creating an asset, memory usage is: 193074
after issue to 1000 clients, memory usage is: 432834
after claimed 1000 clients's token, memory usage is: 193074
```
As the log shows, all memory is reclaim.

