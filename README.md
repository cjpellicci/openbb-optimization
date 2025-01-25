# OpenBB Optimization

## Introduction

This extension introduces portfolio optimization capabilities to the OpenBB platform. The extension utilizes the PyPortfolioOpt function library to provide many popular optimization frameworks, such as mean-variance optimization and Black-Litterman asset allocation models.  

With it you can:

- Determine optimal weights of individual investments across multiple asset classes
- Introduce custom constraints or goals to your model of choice (ie. max return, max sharpe, min volatility)
- Calculate return and risk statistics of the optimal portfolio 

## Getting Started

The extension's functionality can be accessed through a newly created "optimization" sub-module of the OpenBB platform. 

Example of utilizing the extension's mean-variance optimization functionality: