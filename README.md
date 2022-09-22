# Product-Verification-System
App that tells you whether a purchasable physical entity is authentic or not.
Made by Joshua Alwinking...

 # Inspiration
Everybody has bought a fake product before under the premise that it was authentic. We wanted to remove those possibilities of fake products even entering the market as a solution.

# What it does
This system does cross-referencing to the stored database that has the product_id and batch_id of every product known to mankind!

# How we built it
We Started With a Pygame setup that allowed users to run the python program aided by cv and scan qrcodes. We wanted this program to be versatile as the main intension was to be able to scan the product before the purchase to be able to identify the authenticity. Hence we changed to an android kivy application that does the same.

# Challenges we ran into
Initially, we couldn't get the pyagme window to pair with the open cv module and scan barcodes as the mainloop function used up too much ram. Deciding to run the PVS(Product Verification System) as a compact app was a breakthrough we needed.

# Accomplishments that we're proud of
We simplified our tasks and were able to pair it into a versatile app that is ready to be implemented irl.

# What we learned
To easily pair different functional modules into one application
