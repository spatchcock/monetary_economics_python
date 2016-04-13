---
layout: page-fullwidth
title: "Introducing government money"
subheadline: "A simple model with government spending and taxation"
date: 2016-04-12
---

<div class="text_cell_render border-box-sizing rendered_html">
<p>In the previous models we postulated a fixed money supply. In this model we'll include a government sector which creates the money that is used in the economy. So this is our first model in which the amount of money in the economy is <em>dynamic</em> as opposed to fixed. And the first model to include government. We'll consider the basic ways in which a sovereign currency issuing government interacts with the private sector. We'll take a step back from the inclusion of private sector saving that has been a feature of some earlier models, and assume that our private sector has no saving intention. The reason for this is to make the model as simple as possible. This way, the implications of a government and government issued money can be isolated and identifed more easily. We'll consider how a saving economy interacts with its government later.</p>
<p>So, in this model there is a government sector and a non-government (&quot;private&quot;) sector. The government spends by creating money which is then available to circulate in the economy. The government also collects an <em>income tax</em>, that is, it taxes at a fixed rate relative to the income of the non-government sector. The non-government sector pays taxes, and engages in consumer spending using its after-tax, <em>disposable income</em>. That is all, mostly.</p>
<p>This model also introduces the concept of government debt, which is simply the net quantity of money issued to the non-government sector. It might seem strange to call the money issued by the government &quot;debt&quot;. And perhaps it is (?). In more complicated models it will hopefully become clear that what we ordinarily think of as &quot;the government debt&quot; is quite consistent with what is happening in this model (albeit simplified). There is another sense in which government issued money can be considered akin to a debt, though. Governments impose a legally enforcable tax burden on the private sector which can usually only be neutralised in the government's own sovereign currency. By issuing currency to the private sector, the government effectively becomes indebted to the private sector: each unit of currency represents a claim on tax forgiveness to the same amount which the government must honour. In this sense, government issued money can be considered a liability of the government, or, in other words, a debt. Enough of the digression.</p>
</div>
<!--more-->
<div class="text_cell_render border-box-sizing rendered_html">
<p>In this model we'll choose a level of government spending and a tax rate, and these will remain constant for the duration of the model. This type of variable (not really <em>variable</em> at all) is called an <em>exogenous</em> variable - it is defined outside of the model system and is not affected by the other variables or otherwise changed during the course of the model (unless <em>we</em> change it). We can rationalise this decision in our case by considering the values we choose as representing government (fiscal) policy. On the other hand, there are <em>endogenous</em> variables. These are variables that are explicitly calculated <em>by</em> the model and may change during the course of the model run according to the dynamics of the model. The values of these variables are therefore unknown at the outset, they are the things we want the model to find out for us.</p>
<p>So what we need to model - our endogenous variables - are:</p>
<ul>
<li>consumer spending</li>
<li>income</li>
<li>government taxation</li>
<li>disposable income</li>
<li>government debt</li>
</ul>
<p>5 unknowns, so we need 5 equations. We'll start by defining income in our economy. In contrast to previous models where income was simply identically equal to consumer spending, we now have an additional source of income for the private sector:</p>
<p><span class="math">\[Y = C + G \hspace{1cm} (1)\]</span></p>
<p>So at any given point in time, the total income of the economy is equal to the spending which arises from private citizens (and businesses) buying goods and services from one another (<span class="math">\(C\)</span>), as well as sales of goods and services to the government (<span class="math">\(G\)</span>). This income is taxed by the government at a rate <span class="math">\(\theta\)</span>, which is a decimal fraction between <span class="math">\(0\)</span> and <span class="math">\(1\)</span>. So the tax take (<span class="math">\(T\)</span>) at any given point in time is defined as:</p>
<p><span class="math">\[T = \theta Y \hspace{1cm} (2)\]</span></p>
<p>The amount of income which is actually available for spending is the remainder after tax has been paid. This can be called <em>disposable income</em> (<span class="math">\(Y_D\)</span>) and is defined as:</p>
<p><span class="math">\[Y_{d} = Y - T \hspace{1cm} (3)\]</span></p>
<p>Since we're assuming no saving in this model, our citizens simply spend all of their disposable income. As such, the consumption function for this economy is:</p>
<p><span class="math">\[C = Y_{d} \hspace{1cm} (4)\]</span></p>
<p>The last variable we need to calculcate is the government debt. For any given time period, the government debt changes by however much money the government is spending into existence <em>minus</em> however much it collects back in tax. The discernable will realise that this difference is called the <em>government budget deficit</em> (or surplus). In any case, we'll label the government debt <span class="math">\(H_{g}\)</span>, and what we can formally say about it is that it <em>changes</em> in size according to the government's budget position:</p>
<p><span class="math">\[\Delta H_{g} = G - T \hspace{1cm} (5)\]</span></p>
<p>Good. All 5 unknowns are accounted for by our 5 equations.</p>
</div>
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="A-model-in-Python">A model in Python<a class="anchor-link" href="#A-model-in-Python">&#182;</a></h2>
</div>

<div class="text_cell_render border-box-sizing rendered_html">
<p>We're going to iterate through some number of time steps and solve our equations on each one, then see where these equations take our economy. First we need to discritize the equations so we can solve them incrementally. There are a few more things to calculate and keep track of on each time step compared with the previous models, so we need to consider in what order to solve each equation. We also need to think about what initial conditions this model requires.</p>
<p>We'll follow the convention set in previous models whereby income is calculated concurrently with spending, i.e. in the same time step, but that that income is spent in the following time step. This reference across time steps is what drives the circulation of money through time in our model. We could do it the other way around - income based on spending in the <em>previous</em> time step, spending based on income in <em>this</em> time step - but this way sits well intuitively since spending literally (by accounting identity) <em>causes</em> an immediate, equivalent income to be earned in the economy. Income, on the other hand, doesn't itself <em>cause</em> spending but simply enables it to occur subsequently. In any case, and in contrast previous models, there are few extra calculations we need to make on each cycle of spending because it is now only the <em>disposable</em> income which gets carried forward to be spent. So, on each time step we need to first calculate comsumer spending based on the disposable income of the last time step. Once we've established the spending level we can assign the income for that time step, pay income tax, and determine the disposable income to be propagated into the next time step.</p>
<p>So, the difference equation for consumer spending (equation 4) in this model looks like this:</p>
<p><span class="math">\[C_t = Y_{d, t-1}\]</span></p>
<p>All of the variables in the discritized versions of equations 1-3 simply reference the current time step (<span class="math">\(t\)</span>), so there's no need to write them all out explicitly here. The government debt equation (equation 5), on the other hand, is an adjustment equation - it tells us only the <em>change</em> in government debt at any given time. So to calculate the size of the government debt at any given time step we need to add the change to the existing quantity calculated in the previous time step:</p>
<p><span class="math">\[H_{g,t} = H_{g,t-1} + T_t - G\]</span></p>
<p>Good. And what initial conditions do we need? Well, one of the major differences in this model, compared with previous ones, is that money is created in this model. This means that we don't have to specify a stock of money at the outset (which we implicitly did in earlier models by specifying the initial spend). Instead, we can start off with no money in the economy and allow our assumptions to get the economy going. So we'll start off with all variables (<span class="math">\(Y\)</span>, <span class="math">\(C\)</span>, <span class="math">\(T\)</span>, <span class="math">\(Y_d\)</span>, <span class="math">\(H_g\)</span>) having initial values of zero. We really are starting from scratch.</p>
<p>Okay, let's code it up... As before, we first import our libraries, and define the number of time steps we want.</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[1]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="kn">import</span> <span class="nn">matplotlib.pyplot</span> <span class="kn">as</span> <span class="nn">plt</span>
<span class="kn">import</span> <span class="nn">numpy</span> <span class="kn">as</span> <span class="nn">np</span>
<span class="o">%</span><span class="k">matplotlib</span> <span class="n">inline</span>  

<span class="n">N</span> <span class="o">=</span> <span class="mi">100</span>
</pre></div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>Next, we'll define the government's fiscal (taxing and spending) policy, that is the level of government spending (<span class="math">\(G\)</span>) and the tax rate (<span class="math">\(\theta\)</span>). These values are arbitrary, we'll go for 20 pounds and 20% respectively.</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[2]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="n">G</span> <span class="o">=</span> <span class="mi">20</span>
<span class="n">theta</span> <span class="o">=</span> <span class="mf">0.2</span>
</pre></div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>Now we need to establish some arrays to hold the values of our unknown variables as we solve the model at each time step. As before, we simply create arrays of length <code>N</code> initially populated by zeros. This conveniently sets the initial value of each of these variables - the value at <span class="math">\(t=0\)</span>, the first value in each array - to zero, as they should be given that no activity has yet taken place. The subsequent values will be overwritten as we propagate our model.</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[3]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="n">C</span>   <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">N</span><span class="p">)</span> <span class="c"># consumption</span>
<span class="n">Y</span>   <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">N</span><span class="p">)</span> <span class="c"># income</span>
<span class="n">Y_d</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">N</span><span class="p">)</span> <span class="c"># disposable income</span>
<span class="n">T</span>   <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">N</span><span class="p">)</span> <span class="c"># tax revenue</span>
<span class="n">H_g</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">N</span><span class="p">)</span> <span class="c"># government debt</span>
</pre></div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>Now were in a position to iterate through each time step and solve the equations, populating our arrays as we go. Now, we're going to do something cheeky. We're going to iterate from <span class="math">\(t = 0\)</span>. This shouldn't really work, because our code references the previous time step (<span class="math">\(t - 1\)</span>), and it <em>wouldn't</em> work in our earlier models which required specific, non-zero initial conditions. But we're subtley exploiting a feature of the Python language to make life easier for ourselves. See if you can figure out why it works in this case.</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[4]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="k">for</span> <span class="n">t</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">N</span><span class="p">):</span>
    
    <span class="c"># calculate consumer spending</span>
    <span class="n">C</span><span class="p">[</span><span class="n">t</span><span class="p">]</span>   <span class="o">=</span> <span class="n">Y_d</span><span class="p">[</span><span class="n">t</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> 
    
    <span class="c"># calculate total income (consumer spending plus constant government spending)</span>
    <span class="n">Y</span><span class="p">[</span><span class="n">t</span><span class="p">]</span>   <span class="o">=</span> <span class="n">G</span> <span class="o">+</span> <span class="n">C</span><span class="p">[</span><span class="n">t</span><span class="p">]</span> 
    
    <span class="c"># calculate the tax take</span>
    <span class="n">T</span><span class="p">[</span><span class="n">t</span><span class="p">]</span> <span class="o">=</span> <span class="n">theta</span> <span class="o">*</span> <span class="n">Y</span><span class="p">[</span><span class="n">t</span><span class="p">]</span>
    
    <span class="c"># calculate disposable income</span>
    <span class="n">Y_d</span><span class="p">[</span><span class="n">t</span><span class="p">]</span> <span class="o">=</span> <span class="n">Y</span><span class="p">[</span><span class="n">t</span><span class="p">]</span> <span class="o">-</span> <span class="n">T</span><span class="p">[</span><span class="n">t</span><span class="p">]</span>
    
    <span class="c"># calculate the change in government debt</span>
    <span class="n">H_g</span><span class="p">[</span><span class="n">t</span><span class="p">]</span> <span class="o">=</span> <span class="n">H_g</span><span class="p">[</span><span class="n">t</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="o">+</span> <span class="n">T</span><span class="p">[</span><span class="n">t</span><span class="p">]</span><span class="o">-</span> <span class="n">G</span>
   
</pre></div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>That's it! We've solved the entire history of our economy. Okay, there's a lot to keep track of. Let's make a few plots.</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[5]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="n">fig</span> <span class="o">=</span> <span class="n">plt</span><span class="o">.</span><span class="n">figure</span><span class="p">(</span><span class="n">figsize</span><span class="o">=</span><span class="p">(</span><span class="mi">12</span><span class="p">,</span> <span class="mi">4</span><span class="p">))</span>


<span class="n">income_plot</span> <span class="o">=</span> <span class="n">fig</span><span class="o">.</span><span class="n">add_subplot</span><span class="p">(</span><span class="mi">131</span><span class="p">,</span> <span class="n">xlim</span><span class="o">=</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">N</span><span class="p">),</span> <span class="n">ylim</span><span class="o">=</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">np</span><span class="o">.</span><span class="n">max</span><span class="p">(</span><span class="n">Y</span><span class="p">)))</span>
<span class="n">income_plot</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">N</span><span class="p">),</span> <span class="n">Y</span><span class="p">,</span> <span class="n">lw</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="n">income_plot</span><span class="o">.</span><span class="n">grid</span><span class="p">()</span>
<span class="c"># label axes</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">&#39;time&#39;</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">&#39;income&#39;</span><span class="p">)</span>

<span class="n">consumption_plot</span> <span class="o">=</span> <span class="n">fig</span><span class="o">.</span><span class="n">add_subplot</span><span class="p">(</span><span class="mi">132</span><span class="p">,</span> <span class="n">xlim</span><span class="o">=</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">N</span><span class="p">),</span> <span class="n">ylim</span><span class="o">=</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">np</span><span class="o">.</span><span class="n">max</span><span class="p">(</span><span class="n">Y</span><span class="p">)))</span>
<span class="n">consumption_plot</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">N</span><span class="p">),</span> <span class="n">C</span><span class="p">,</span> <span class="n">lw</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="n">consumption_plot</span><span class="o">.</span><span class="n">grid</span><span class="p">()</span>
<span class="c"># label axes</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">&#39;time&#39;</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">&#39;consumption&#39;</span><span class="p">)</span>

<span class="n">gov_plot</span> <span class="o">=</span> <span class="n">fig</span><span class="o">.</span><span class="n">add_subplot</span><span class="p">(</span><span class="mi">133</span><span class="p">,</span> <span class="n">xlim</span><span class="o">=</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">N</span><span class="p">),</span> <span class="n">ylim</span><span class="o">=</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">np</span><span class="o">.</span><span class="n">max</span><span class="p">(</span><span class="n">Y</span><span class="p">)))</span>
<span class="n">gov_plot</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">N</span><span class="p">),</span> <span class="n">np</span><span class="o">.</span><span class="n">repeat</span><span class="p">(</span><span class="n">G</span><span class="p">,</span><span class="n">N</span><span class="p">),</span> <span class="n">lw</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="n">gov_plot</span><span class="o">.</span><span class="n">grid</span><span class="p">()</span>
<span class="c"># label axes</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">&#39;time&#39;</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">&#39;government spending&#39;</span><span class="p">)</span>

<span class="c"># space subplots neatly</span>
<span class="n">plt</span><span class="o">.</span><span class="n">tight_layout</span><span class="p">()</span>
</pre></div>

</div>
</div>

<div class="vbox output_wrapper">
<div class="output vbox">


<div class="hbox output_area"><div class="prompt"></div>
<div class="box-flex1 output_subarea output_display_data">


<img src="data:image/png;base64,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
4Gn2sXdmkQAAAABJRU5ErkJggg==
">

</div>
</div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>These plots show income (left) and combined, overall spending (consumption, middle; government spending, right). Just looking at the income plot we see something that we haven't seen yet in any previous models: a growing economy. Income is only 20 pounds at the start but <em>increases</em> rapidly over the first 20 or so time steps to a value of 100 pounds per time step. After this, income remains constant and we have what looks like a steady-state economy. So something is causing income in our economy to <em>grow</em>, and something is causing it to stabilize at some level. Let's follow the logic of our equations and try to figure out what happened.</p>
<p>In the first time step there was no consumption because there was no previous spending or incomes. How could there be? There was no money to spend. But there was government spending of 20 pounds, which introduce 20 pounds of currency and provided 20 pounds of income. This income was immediately taxed to the tune of 4 pounds (20%) leaving 16 pounds of disposable income to carry over to the next time step. In the second time step this 16 pounds was spent and together with further government spending of 20 pounds became a total income of 36 pounds in our economy. This 36 pounds of income was taxed at 20% (7.20 pounds) leaving 28.80 as disposable income. In the next time step, the 28.80 pounds of disposable income left over from last time was spent providing a total income of 48.80 with the 20 pounds of government spending. 9.76 pounds of tax were paid on this income leaving 39.04 pounds of disposable income. And so on...</p>
<table>
<thead>
<tr class="header">
<th align="left">time step</th>
<th align="right">consumption</th>
<th align="right">government</th>
<th align="right">income</th>
<th align="right">tax take</th>
<th align="right">disposable income</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="left">1</td>
<td align="right">0.00</td>
<td align="right">20.00</td>
<td align="right">20.00</td>
<td align="right">4.00</td>
<td align="right">16.00</td>
</tr>
<tr class="even">
<td align="left">2</td>
<td align="right">16.00</td>
<td align="right">20.00</td>
<td align="right">36.00</td>
<td align="right">7.20</td>
<td align="right">28.80</td>
</tr>
<tr class="odd">
<td align="left">3</td>
<td align="right">28.80</td>
<td align="right">20.00</td>
<td align="right">48.80</td>
<td align="right">9.76</td>
<td align="right">39.04</td>
</tr>
<tr class="even">
<td align="left">4</td>
<td align="right">39.04</td>
<td align="right">20.00</td>
<td align="right">59.04</td>
<td align="right">11.81</td>
<td align="right">47.23</td>
</tr>
<tr class="odd">
<td align="left">...</td>
<td align="right">...</td>
<td align="right">...</td>
<td align="right">...</td>
<td align="right">...</td>
<td align="right">...</td>
</tr>
<tr class="even">
<td align="left">100</td>
<td align="right">80.00</td>
<td align="right">20.00</td>
<td align="right">100.00</td>
<td align="right">20.00</td>
<td align="right">80.00</td>
</tr>
</tbody>
</table>
<p>Eventually,the economy settles down to a constant, steady-state income of 100 pounds per time step. Looking at the plots above, we can see that this income is made up of a constant, steady-state consumption spend of 80 pounds per time step and the 20 pounds per time step that the government spends. So during the course of our model, consumption spending rose from 0 pounds to a stable 80 pounds.</p>
<p>Now let's take a look at the government accounts.</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[6]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="n">fig</span> <span class="o">=</span> <span class="n">plt</span><span class="o">.</span><span class="n">figure</span><span class="p">(</span><span class="n">figsize</span><span class="o">=</span><span class="p">(</span><span class="mi">8</span><span class="p">,</span> <span class="mi">8</span><span class="p">))</span>

<span class="n">gov_plot</span> <span class="o">=</span> <span class="n">fig</span><span class="o">.</span><span class="n">add_subplot</span><span class="p">(</span><span class="mi">221</span><span class="p">,</span> <span class="n">xlim</span><span class="o">=</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">N</span><span class="p">),</span> <span class="n">ylim</span><span class="o">=</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">np</span><span class="o">.</span><span class="n">max</span><span class="p">(</span><span class="n">G</span><span class="p">)</span><span class="o">*</span><span class="mf">1.5</span><span class="p">))</span>
<span class="n">gov_plot</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">N</span><span class="p">),</span> <span class="n">np</span><span class="o">.</span><span class="n">repeat</span><span class="p">(</span><span class="n">G</span><span class="p">,</span><span class="n">N</span><span class="p">),</span> <span class="n">lw</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="n">gov_plot</span><span class="o">.</span><span class="n">grid</span><span class="p">()</span>
<span class="c"># label axes</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">&#39;time&#39;</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">&#39;government spending&#39;</span><span class="p">)</span>

<span class="n">tax_plot</span> <span class="o">=</span> <span class="n">fig</span><span class="o">.</span><span class="n">add_subplot</span><span class="p">(</span><span class="mi">222</span><span class="p">,</span> <span class="n">xlim</span><span class="o">=</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">N</span><span class="p">),</span> <span class="n">ylim</span><span class="o">=</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">np</span><span class="o">.</span><span class="n">max</span><span class="p">(</span><span class="n">G</span><span class="p">)</span><span class="o">*</span><span class="mf">1.5</span><span class="p">))</span>
<span class="n">tax_plot</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">N</span><span class="p">),</span> <span class="n">T</span><span class="p">,</span> <span class="n">lw</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="n">tax_plot</span><span class="o">.</span><span class="n">grid</span><span class="p">()</span>
<span class="c"># label axes</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">&#39;time&#39;</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">&#39;tax revenue&#39;</span><span class="p">)</span>

<span class="n">deficit_plot</span> <span class="o">=</span> <span class="n">fig</span><span class="o">.</span><span class="n">add_subplot</span><span class="p">(</span><span class="mi">223</span><span class="p">,</span> <span class="n">xlim</span><span class="o">=</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">N</span><span class="p">),</span> <span class="n">ylim</span><span class="o">=</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">min</span><span class="p">(</span><span class="n">H_g</span><span class="p">)</span><span class="o">*</span><span class="mf">1.5</span><span class="p">,</span><span class="mi">0</span><span class="p">))</span>
<span class="n">deficit_plot</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">N</span><span class="p">),</span> <span class="n">T</span><span class="o">-</span><span class="n">np</span><span class="o">.</span><span class="n">repeat</span><span class="p">(</span><span class="n">G</span><span class="p">,</span><span class="n">N</span><span class="p">),</span> <span class="n">lw</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="n">deficit_plot</span><span class="o">.</span><span class="n">grid</span><span class="p">()</span>
<span class="c"># label axes</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">&#39;time&#39;</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">&#39;government budget&#39;</span><span class="p">)</span>

<span class="n">debt_plot</span> <span class="o">=</span> <span class="n">fig</span><span class="o">.</span><span class="n">add_subplot</span><span class="p">(</span><span class="mi">224</span><span class="p">,</span> <span class="n">xlim</span><span class="o">=</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">N</span><span class="p">),</span> <span class="n">ylim</span><span class="o">=</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">min</span><span class="p">(</span><span class="n">H_g</span><span class="p">)</span><span class="o">*</span><span class="mf">1.5</span><span class="p">,</span><span class="mi">0</span><span class="p">))</span>
<span class="n">debt_plot</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">N</span><span class="p">),</span> <span class="n">H_g</span><span class="p">,</span> <span class="n">lw</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="n">debt_plot</span><span class="o">.</span><span class="n">grid</span><span class="p">()</span>
<span class="c"># label axes</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">&#39;time&#39;</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">&#39;government debt&#39;</span><span class="p">)</span>


<span class="c"># space subplots neatly</span>
<span class="n">plt</span><span class="o">.</span><span class="n">tight_layout</span><span class="p">()</span>
</pre></div>

</div>
</div>

<div class="vbox output_wrapper">
<div class="output vbox">


<div class="hbox output_area"><div class="prompt"></div>
<div class="box-flex1 output_subarea output_display_data">


<img src="data:image/png;base64,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
OQZKSUkxOoJbJOWVlBWQl5fkkHZuMa9a0vJ6SlSRs3r1ajRv3hxhYWGYNm2a0XE8dvr0aaMjuEVS
XklZAXl5rc5KfY20c4t51ZKW11Niipz8/HyMGTMGq1evRmpqKpYsWYI9e/YYHYuILIZ9DZF1iCly
tm7diiZNmiAkJAR+fn544IEHsHLlSqNjeSQ9Pd3oCG6RlFdSVkBeXiuzWl8j7dxiXrWk5fWUmK+Q
L1++HP/9738xd+5cAMDHH3+M77//HrNnz3b9jMPhMCoeke0I6TrcVlZfw36GSF+e9DW+Xsyh1I10
LFbtdIlIP2X1NexniOQQM1zVoEEDZGRkuNYzMjIQHBxsYCIisiL2NUTWIabIiY6Oxv79+5Geno68
vDwsXboUffr0MToWEVkM+xoi6xAzXOXr64u3334bvXr1Qn5+PkaMGIEWLVoYHYuILIZ9DZF1iLmS
AwC9e/fG3r178euvv+KFF14o8Xdmv69FRkYGunfvjpYtW6JVq1Z46623AAAnT55EbGwsmjZtip49
e5rqHgb5+flo27Yt4uLiAJg76+nTp3H//fejRYsWCA8Px/fff2/qvFOmTEHLli0RERGBBx98EL//
/rup8g4fPhyBgYGIiIhwbbtevilTpiAsLAzNmzfHmjVrjIjsVdfqa9jPqMG+Rh279zWiipxrkXBf
Cz8/P8ycORO7d+/Gli1b8M4772DPnj2YOnUqYmNjsW/fPtx5552YOnWq0VFdZs2ahfDwcNdETDNn
HTduHO6++27s2bMHu3btQvPmzU2bNz09HXPnzsWOHTvw008/IT8/H59++qmp8g4bNgyrV68use1a
+VJTU7F06VKkpqZi9erVGD16NAoKCoyIrRT7GXXY16jBvgaAZgGbN2/WevXq5VqfMmWKNmXKFAMT
le2+++7T1q5dqzVr1kzLzs7WNE3TsrKytGbNmhmczCkjI0O78847tW+++Ua79957NU3TTJv19OnT
Wmho6FXbzZr3t99+05o2baqdPHlS++OPP7R7771XW7NmjenypqWlaa1atXKtXyvf5MmTtalTp7p+
rlevXtp3332nb1gdsJ9Rg32NOuxrNM0SV3IyMzNxyy23uNaDg4ORmZlpYKLrS09Px86dO9GxY0fk
5OQgMDAQABAYGIicnByD0zk9/fTTeOONN+DjU3SKmDVrWloa6tSpg2HDhqFdu3YYOXIkzp8/b9q8
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
">

</div>
</div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>The top left plot shows government spending, which, as we know, is simply constant throughout the duration of the model. It is an endogenous variable and that's how we set it. The top right plot shows the government's tax revenue. Since it is proportionate to income, the tax revenue was small (4 pounds) at the start when incomes were small (20 pounds) but increased as income itself grew. Eventually tax revenue stablises at 20 pounds per time step, which is 20% of the steady-state income of 100 pounds, consistent with our tax rate.</p>
<table>
<thead>
<tr class="header">
<th align="left">time step</th>
<th align="right">government spending</th>
<th align="right">tax revenue</th>
<th align="right">budget outcome</th>
<th align="right">government debt</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="left">1</td>
<td align="right">20.00</td>
<td align="right">4.00</td>
<td align="right">-16.00</td>
<td align="right">-16.00</td>
</tr>
<tr class="even">
<td align="left">2</td>
<td align="right">20.00</td>
<td align="right">7.20</td>
<td align="right">-12.80</td>
<td align="right">-28.80</td>
</tr>
<tr class="odd">
<td align="left">3</td>
<td align="right">20.00</td>
<td align="right">9.76</td>
<td align="right">-10.24</td>
<td align="right">-39.04</td>
</tr>
<tr class="even">
<td align="left">4</td>
<td align="right">20.00</td>
<td align="right">11.81</td>
<td align="right">-8.19</td>
<td align="right">-47.23</td>
</tr>
<tr class="odd">
<td align="left">...</td>
<td align="right">...</td>
<td align="right">...</td>
<td align="right">...</td>
<td align="right">...</td>
</tr>
<tr class="even">
<td align="left">100</td>
<td align="right">20.00</td>
<td align="right">20.00</td>
<td align="right">0.00</td>
<td align="right">-80.00</td>
</tr>
</tbody>
</table>
<p>The bottom left plot shows the <em>government budget outcome</em>. That is the difference between spending and tax revenue. As we can see, the budget outcome is negative at the start meaning that the government has a budget <em>deficit</em>. This deficit is gradually reduced until the budget becomes balanced - the 20 pounds steady-state tax revenue is exactly equal to government's own spend. This budget deficit means that more money is being spent <em>into</em> the economy than is being taxed <em>out</em> of it. This is reflected in the bottom right plot which shows the government debt. The government debt increases as long as the government budget is in deficit. Once the budget is balanced, the debt no longer grows and reaches a steady-state. The eventual size of the government debt is 80 pounds.</p>
<p>So what is going on here? Why do we have a growth of incomes and why does it stablize? In a sense, this model is the opposite of the model which included savings. In that model, the attempt to save on each time step meant that spending in each time step was less than in the previous time step. This caused incomes to gradually decline. In this model, the amount of spending <em>increases</em> in each time step, at least during the initial stages of the model run. This is because the government is adding new spending in each time step <em>on top of</em> the spending which is taking place anyway by virtue of the spending of incomes earned in the previous time step (the circular flow of money). And each time the government spends new money into the economy, that money is added to the amount which continues to recirculate via the process of repeated spending, and so the growth is permanent. This is reflected in the increase in consumption spending seen. The government is adding to overall spending in this way any time it has a budget deficit: in such a case spending is greater than taxation and therefore represents a <em>net</em> spend into the economy.</p>
<p>So as long as the government is in deficit, overall spending, and therefore incomes, are growing. But the deficit reduces through time in our model. This is because tax revenue is related to income: as incomes grow, so does tax revenue. With government spending constant and tax revenues growing, at some point tax revenues reach the same size as the government spending (i.e. 20 pounds). This is the point at which the government's budget is balanced and therefore the point at which the government ceases to be adding spending to the economy: what is added with spending is <em>exactly</em> removed with tax. At this point, with no additional net spending, the overall spending in the economy (consumption + government) remains stable, as do incomes. And with income stabilizing, so does tax revenue, so government budget <em>stays</em> balanced.</p>
</div>
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="The-fiscal-multiplier">The fiscal multiplier<a class="anchor-link" href="#The-fiscal-multiplier">&#182;</a></h2>
</div>

<div class="text_cell_render border-box-sizing rendered_html">
<p>So, in this model, government spending acts as a stimulus to spending and incomes whereas taxation acts to constrain them. These two forces end up balancing at a particular level of incomes. To see how this works we can do a bit of algebra. We'll use the <span class="math">\(^*\)</span> notation to signify steady-state values of our variables. So at steady-state, we have the equations:</p>
<p><span class="math">\[
\begin{array}{lcl}
Y^* = C^* + G \hspace{1cm} &amp; (6) \\
T^* = \theta Y^* \hspace{1cm} &amp; (7) \\
Y_{d}^* = Y^* - T^* \hspace{1cm} &amp; (8) \\
C^* = Y_{d}^* \hspace{1cm} &amp; (9) \\
\end{array}
\]</span></p>
<p>By substituting equation 7 into equation 8 we get:</p>
<p><span class="math">\[Y_{d}^* = Y^* - \theta Y^*\]</span></p>
<p>which we can then substitue into equation 9:</p>
<p><span class="math">\[C^* = Y^* - \theta Y^*\]</span></p>
<p>and then back into equation 6:</p>
<p><span class="math">\[Y^* = Y^* - \theta Y^* + G\]</span></p>
<p>Rearranging this gives:</p>
<p><span class="math">\[ Y^* = \frac {G}{\theta} \hspace{1cm} (10)\]</span></p>
<p>So the steady state income of our model is determined by the ratio of government spending to the government imposed taxation rate. Let's check this in our model. First we'll calculate the result of equation 10 using our model parameters.</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[7]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="k">print</span><span class="p">(</span><span class="n">G</span><span class="o">/</span><span class="n">theta</span><span class="p">)</span>
</pre></div>

</div>
</div>

<div class="vbox output_wrapper">
<div class="output vbox">


<div class="hbox output_area"><div class="prompt"></div>
<div class="box-flex1 output_subarea output_stream output_stdout">
<pre>
100.0

</pre>
</div>
</div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>And now we'll just inspect the last value in the income array from our model run. In Python, the last element of an array is accessed using the <code>-1</code> index.</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[8]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="k">print</span><span class="p">(</span><span class="n">Y</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">])</span>
</pre></div>

</div>
</div>

<div class="vbox output_wrapper">
<div class="output vbox">


<div class="hbox output_area"><div class="prompt"></div>
<div class="box-flex1 output_subarea output_stream output_stdout">
<pre>
99.9999999796

</pre>
</div>
</div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>Well that's close enough. The final, steady-state income in our economy is equal to the rate of government spending divided by the tax rate, as described by equation 10. We can generalise this a bit more by dividing equation 10 by our government spending rate. This gives us the value of steady-state income <em>relative to the government spending</em>:</p>
<p><span class="math">\[\frac{Y^*}{G} = \frac {1}{\theta}\]</span></p>
<p>So the expression <span class="math">\(\frac {1}{\theta}\)</span> tells us how big income will be relative to the government spend (without actually having to run the model). In our case, the left-hand side of that equation is:</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[9]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="k">print</span><span class="p">(</span><span class="n">Y</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span><span class="o">/</span><span class="n">G</span><span class="p">)</span>
</pre></div>

</div>
</div>

<div class="vbox output_wrapper">
<div class="output vbox">


<div class="hbox output_area"><div class="prompt"></div>
<div class="box-flex1 output_subarea output_stream output_stdout">
<pre>
4.99999999898

</pre>
</div>
</div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>and the right-hand side is:</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[10]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="k">print</span><span class="p">(</span><span class="mi">1</span><span class="o">/</span><span class="n">theta</span><span class="p">)</span>
</pre></div>

</div>
</div>

<div class="vbox output_wrapper">
<div class="output vbox">


<div class="hbox output_area"><div class="prompt"></div>
<div class="box-flex1 output_subarea output_stream output_stdout">
<pre>
5.0

</pre>
</div>
</div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>Equal, as predicted. So, incomes in our model are <span class="math">\(5 \times\)</span> the size of the government spend, and this would be the case whatever level of government spending we had chosen. We can call this value the <em>fiscal multiplier</em> and it represents the amount of economic activity which is stimulated by each pound of spending by the government. Put another way, each pound spent by the government is spent again 5 times before it ultimately returns to the government as tax revenue, supporting incomes on the way. In more complex models the fiscal multiplier doesn't necessarily take on such a simple form.</p>
</div>
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Conclusions">Conclusions<a class="anchor-link" href="#Conclusions">&#182;</a></h2>
</div>

<div class="text_cell_render border-box-sizing rendered_html">
<p>We postulated a currency issuing government which spends money into existence and taxes it back out of the economy. Spending was set at a fixed, <em>absolute</em> value per time step whereas taxation was stipulated as a fixed <em>fraction</em> of economy activity (income). The government spending stimulated additional spending activity in the economy and the economy grew to a size which was a multiple of the government spend. An initial budget deficit was <em>automatically</em> reduced and the budget was balanced without any change in government policy. The government debt reached a fixed, stable level relative to the size of the economy and represented all the money required to support spending in the economy.</p>
<p>Because the government was the &quot;sovereign&quot; currency issuer, it needed to spend before any economic activity could take place. Otherwise, there was no money in existence at all. Indeed, it was even necessary for the government to spend before any tax could be paid! In this economy, therefore, government spending is not funded by tax revenues, which, in any case, is an incoherent concept for a currency issuer. Examples of sovereign currency issuing governments are those of the US, UK, Australia and Japan. The countries of the Eurozone do not fit this description.</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre>
</pre></div>

</div>
</div>

</div>