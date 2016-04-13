---
layout: page-fullwidth
title: "The Paradox of Thrift"
subheadline: "Why saving has a price"
date: 2016-04-11
---

<div class="text_cell_render border-box-sizing rendered_html">
<p><strong>TL;DR</strong> * In an economy with a fixed money supply saving causes a reduction in spending and therefore incomes * As incomes reduce any further attempt to save is hindered * The ability of the economy to save is inherently limited by the cost it has on incomes</p>
</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>In the last model we simply watched money circulate around our economy. Because the same amount of money was spent in each time period, income was constant and there was nothing in the model to change this status quo. In this model, we'll allow our citizens an additional freedom. Instead of spending every pound they earn, they will have two options for how to use their income: they can save some part of it, and spend the rest.</p>
<p>We need a new consumption function. In the last model we defined consumption as simply being exactly equal to income (<span class="math">\(C = Y\)</span>). We can generalise this by stating that consumption spending is equal to some fraction, <span class="math">\(\alpha\)</span>, of income:</p>
<p><span class="math">\[C = \alpha Y \hspace{1cm} (1)\]</span></p>
<p>where <span class="math">\(0 \gt \alpha \lt 1\)</span>. Our previous model, which implied complete, 100% spending of income with no savings, can now be seen as a special case in which <span class="math">\(\alpha = 1\)</span>. But if, for example, citizens in our economy decide to spend (on average) only 95% of their income (saving 5%), then we'd have <span class="math">\(\alpha = 0.95\)</span> and spending would equal <span class="math">\(0.95Y\)</span>.</p>
<p>Like before, all spending becomes income, simply by the identity which links buyers with sellers. So we continue with the income equation:</p>
<p><span class="math">\[Y = C \hspace{1cm} (2)\]</span></p>
<p>But we have a third unknown in our economy now. The money that is not spent has to go somewhere. It cannot simply vanish. So we must define a variable to keep track of it. Effectively, we are considering unspent money to represent savings, and so we'll keep track of how much is saved. We'll label the accumulated savings of the economy <span class="math">\(H\)</span>. We need an equation which describes how <span class="math">\(H\)</span> is calculcated during our model run.</p>
<p>If we know how much of income is being <em>spent</em> at any given moment (equation 1), then we can easily work out how much is being <em>saved</em> at any moment. It is simply <span class="math">\((1 - \alpha) Y\)</span>. If 95% is being spent then 5% is being saved, for example. And if we know how much is <em>being saved</em> at any instant, then don't necessarily how much total savings we have accumulated, but we know how much that amount is <em>changing</em>. The standard way of notating a <em>change in a quantity</em> is to use the Greek &quot;delta&quot; character <span class="math">\(\Delta\)</span>. So our third equation will be:</p>
<p><span class="math">\[\Delta H = (1 - \alpha)Y \hspace{1cm} (3)\]</span></p>
<p>Equation 3 simply tells us by how much the accumulated wealth of the economy changes in relation to current income. Okay, we have 3 unknowns (<span class="math">\(C\)</span>, <span class="math">\(Y\)</span>, <span class="math">\(H\)</span>) and 3 equations. We can code these up now and see what happens.</p>
</div>
<!--more-->
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="A-model-in-Python">A model in Python<a class="anchor-link" href="#A-model-in-Python">&#182;</a></h2>
</div>

<div class="text_cell_render border-box-sizing rendered_html">
<p>Again, we'll iterate through some number of time steps and solve our equations as we go. Each variable needs to be updated at each time step so that we can understand the path of our economy. As before, we need to <em>discretize</em> our equations, that is, convert them into <em>difference equations</em> which can be computed across discrete time steps.</p>
<p>Calculating <span class="math">\(C\)</span> in each time step is straightforward. As before, it is related to the income from the previous time step, but with a twist - only a fraction (<span class="math">\(\alpha\)</span>) of the income from the previous time step is spent:</p>
<p><span class="math">\[C_t = \alpha Y_{t-1}\]</span></p>
<p>As before, spending is still immediately equated with income, and so we retain</p>
<p><span class="math">\[Y_t = C_t\]</span></p>
<p>And finally we need to calculate the stock of savings. From equation (3) we know how savings change on each time step. So it is fairly trivial to calculate what the total amount of accumulated savings are at any given time step by simply adding the current change in savings to the existing savings from the previous time step:</p>
<p><span class="math">\[H_t = H_{t-1} + (1 - \alpha) Y_{t-1}\]</span></p>
<p>Great, we've discretized our model. Now we can code it.</p>
<p>As before, we first import our libraries,</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[8]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="kn">import</span> <span class="nn">matplotlib.pyplot</span> <span class="kn">as</span> <span class="nn">plt</span>
<span class="kn">import</span> <span class="nn">numpy</span> <span class="kn">as</span> <span class="nn">np</span>
<span class="o">%</span><span class="k">matplotlib</span> <span class="n">inline</span>  
</pre></div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>then set the number of time intervals to simulate:</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[9]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="n">N</span> <span class="o">=</span> <span class="mi">100</span>
</pre></div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>Next, we create some arrays to hold the values of our unknown variables in each time step. We want 3 arrays for the 3 unknowns we have, and each needs to be the same length as the number of time steps (<code>N</code>).</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[10]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="n">C</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">N</span><span class="p">)</span> <span class="c"># consumption</span>
<span class="n">Y</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">N</span><span class="p">)</span> <span class="c"># income</span>
<span class="n">H</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">N</span><span class="p">)</span> <span class="c"># stock of accumulated savings</span>
</pre></div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>This model has a parameter, <span class="math">\(\alpha\)</span>, which describes the <em>propensity to consume</em> (out of income). This needs to be set. We'll go with a value of 90%, i.e. 90% of income is used for consumption spending. In decimal fraction notation this is <code>0.90</code>.</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[11]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="n">alpha</span> <span class="o">=</span> <span class="mf">0.90</span>
</pre></div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>And as in the last model, we need to set some initial conditions in order to kickstart our economy. We'll go with the same initial spending spree of 100 pounds. This immediately equates to 100 pounds of income at the outset. So we'll set these initial conditions for <code>C</code> and <code>Y</code>. <code>H</code> does not need an initial condition to be explicitly set. The <code>H</code> array is already filled with zeros and therefore the initial state of accumulated wealth (the first value) is already simply zero. In other words, we're already set up to start off with zero savings. That is fine. We could give it some other starting value but there is not much to be gained by doing so.</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[12]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="n">C</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">=</span> <span class="mi">100</span>
<span class="n">Y</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">=</span> <span class="mi">100</span>
</pre></div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>Okay, we can iterate through time using our difference equations.</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[13]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="k">for</span> <span class="n">t</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">N</span><span class="p">):</span>
    <span class="n">C</span><span class="p">[</span><span class="n">t</span><span class="p">]</span> <span class="o">=</span> <span class="n">alpha</span> <span class="o">*</span> <span class="n">Y</span><span class="p">[</span><span class="n">t</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>                <span class="c"># calculate spending based on earlier income (with some saving)</span>
    <span class="n">Y</span><span class="p">[</span><span class="n">t</span><span class="p">]</span> <span class="o">=</span> <span class="n">C</span><span class="p">[</span><span class="n">t</span><span class="p">]</span>                          <span class="c"># calculcate income earned in this time period</span>
    <span class="n">H</span><span class="p">[</span><span class="n">t</span><span class="p">]</span> <span class="o">=</span> <span class="n">H</span><span class="p">[</span><span class="n">t</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="o">+</span> <span class="p">(</span><span class="mi">1</span> <span class="o">-</span> <span class="n">alpha</span><span class="p">)</span> <span class="o">*</span> <span class="n">Y</span><span class="p">[</span><span class="n">t</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="c"># calculate increase in accumulated savings</span>
</pre></div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>Done. As before, we'll just plot the history of our economy and take a look. We'll create 3 plots this time, to represent our 3 unknown variables (<span class="math">\(C\)</span>, <span class="math">\(Y\)</span>, <span class="math">\(H\)</span>).</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[14]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="c"># create a figure</span>
<span class="n">fig</span> <span class="o">=</span> <span class="n">plt</span><span class="o">.</span><span class="n">figure</span><span class="p">(</span><span class="n">figsize</span><span class="o">=</span><span class="p">(</span><span class="mi">12</span><span class="p">,</span> <span class="mi">4</span><span class="p">))</span>

<span class="c"># create a subplot for consumption</span>
<span class="n">consumption_plot</span> <span class="o">=</span> <span class="n">fig</span><span class="o">.</span><span class="n">add_subplot</span><span class="p">(</span><span class="mi">131</span><span class="p">)</span>
<span class="c"># plot consumption (C) versus time step (N)</span>
<span class="n">consumption_plot</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">N</span><span class="p">),</span> <span class="n">C</span><span class="p">,</span> <span class="n">lw</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="c"># add gridlines</span>
<span class="n">consumption_plot</span><span class="o">.</span><span class="n">grid</span><span class="p">()</span>
<span class="c"># ensure a zero origin for the y axis</span>
<span class="n">consumption_plot</span><span class="o">.</span><span class="n">set_ylim</span><span class="p">([</span><span class="mi">0</span><span class="p">,</span> <span class="n">np</span><span class="o">.</span><span class="n">max</span><span class="p">(</span><span class="n">C</span><span class="p">)])</span>
<span class="c"># label axes</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">&#39;time&#39;</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">&#39;consumption&#39;</span><span class="p">)</span>

<span class="c"># create a second subplot for income</span>
<span class="n">income_plot</span> <span class="o">=</span> <span class="n">fig</span><span class="o">.</span><span class="n">add_subplot</span><span class="p">(</span><span class="mi">132</span><span class="p">)</span>
<span class="c"># plot income (Y) versus time step (N)</span>
<span class="n">income_plot</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">N</span><span class="p">),</span> <span class="n">Y</span><span class="p">,</span> <span class="n">lw</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="c"># add gridlines</span>
<span class="n">income_plot</span><span class="o">.</span><span class="n">grid</span><span class="p">()</span>
<span class="c"># ensure a zero origin for the y axis</span>
<span class="n">income_plot</span><span class="o">.</span><span class="n">set_ylim</span><span class="p">([</span><span class="mi">0</span><span class="p">,</span> <span class="n">np</span><span class="o">.</span><span class="n">max</span><span class="p">(</span><span class="n">Y</span><span class="p">)])</span>
<span class="c"># label axes</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">&#39;time&#39;</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">&#39;income&#39;</span><span class="p">)</span>

<span class="c"># create a third subplot for private wealth</span>
<span class="n">savings_plot</span> <span class="o">=</span> <span class="n">fig</span><span class="o">.</span><span class="n">add_subplot</span><span class="p">(</span><span class="mi">133</span><span class="p">)</span>
<span class="c"># plot savings (H) versus time step (N)</span>
<span class="n">savings_plot</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">N</span><span class="p">),</span> <span class="n">H</span><span class="p">,</span> <span class="n">lw</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="c"># add gridlines</span>
<span class="n">savings_plot</span><span class="o">.</span><span class="n">grid</span><span class="p">()</span>
<span class="c"># ensure a zero origin for the y axis</span>
<span class="n">savings_plot</span><span class="o">.</span><span class="n">set_ylim</span><span class="p">([</span><span class="mi">0</span><span class="p">,</span> <span class="mi">100</span><span class="p">])</span>
<span class="c"># label axes</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">&#39;time&#39;</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">&#39;accumulated savings&#39;</span><span class="p">)</span>

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
/gfmlU+CPr2WnwAAAABJRU5ErkJggg==
">

</div>
</div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>Our disciplined citizens have manged to save enough money to have accumulated 100 pounds of savings by the end of the model run. Maybe they should feel very proud of themselves. But look what's happened to their incomes! Incomes have dropped from 100 pounds per time step at the start to 0 at the end of the simulation. This is a recession of catastrophic proportions. Let's walk through what happened.</p>
<table>
<thead>
<tr class="header">
<th align="left">time step</th>
<th align="right">consumption</th>
<th align="right">income</th>
<th align="right">saving</th>
<th align="right">accumulated savings</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="left">1</td>
<td align="right">100.00</td>
<td align="right">100.00</td>
<td align="right">-</td>
<td align="right">-</td>
</tr>
<tr class="even">
<td align="left">2</td>
<td align="right">90.00</td>
<td align="right">90.00</td>
<td align="right">10.00</td>
<td align="right">10.00</td>
</tr>
<tr class="odd">
<td align="left">3</td>
<td align="right">81.50</td>
<td align="right">81.50</td>
<td align="right">8.50</td>
<td align="right">18.50</td>
</tr>
<tr class="even">
<td align="left">4</td>
<td align="right">74.28</td>
<td align="right">74.28</td>
<td align="right">7.22</td>
<td align="right">25.72</td>
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
<td align="right">0.00</td>
<td align="right">0.00</td>
<td align="right">0.00</td>
<td align="right">100.00</td>
</tr>
</tbody>
</table>
<p>In the first time step, 100 pounds was spent and immediately earned as income. In the next time step, 90 pounds were spent - 90% of the earned income from previously - and 10 pounds were added to the savings account. These 90 pounds were immediately earned as income for spending in the next time step. In the 3rd time step, 90% of that 90 pounds of income was spent on and the other 10% saved. That's 81.50 pounds of spending (and, therefore, concurrent income) and 8.50 pounds of saving taking the savings account to 18.50 pounds. In the 4th time step, 90% of the 81.50 pounds earned from the previous time step (74.28 pounds) was spent, with 7.22 being added to savings. And so on.</p>
<p>Because of the intention to accumulate savings, the income available for spending on each time step is smaller than the time step before. This results in a feedback cycle of less income begeting less future spending which begets yet less income and even lower subsequent spending. As the accumulated savings in the economy grows, the amount of money cycling round the economy - supporting spending and incomes - becomes smaller and smaller. Eventually, the entire money stock is held as savings and there is no money circulating at all. This is a completely unstable economy.</p>
<p>The problem highlighted in this model was called <em>The Paradox of Thrift</em> by John Maynard Keynes. The paradox refers to the fact that the attempt of private individuals (and/or businesses) to collectively save causes aggregate incomes to drop. The fall in incomes has at least two effects. If it occurs equally across all individuals then it means that living standards decline: everyone has less purchasing power. More likely, however, is that it will not affect all individuals equally and will instead result in some people becoming unemployed. A more subtle effect of the fall in incomes, however, is simply that it means that less can be saved in future. In these ways, the attempt to save <em>en masse</em> can be considered self-defeating.</p>
</div>
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Reacting-to-the-recession">Reacting to the recession<a class="anchor-link" href="#Reacting-to-the-recession">&#182;</a></h2>
</div>

<div class="text_cell_render border-box-sizing rendered_html">
<p>The model economy simulated above is an extreme scenario and unlikely to occur in practice. The reason is that some amount of spending is utterly necessary, to provide for, well, the necessities in life: food, shelter, energy, etc. It is highly unlikely that individuals would forgo such necessities because of their intention to save. At some point during the decline in incomes it is more likely that folk will start to spend some of the savings that they have accumulated in order to replace some of the lost income. Let's try a new model which reflects this behaviour.</p>
<p>What we want is for some spending out of the stock of savings to occur. And what would seem intuitively consistent with the scenario postulated above is that more is spent out of savings when incomes are lower and less when incomes are higher. Put another way, more is spent out of savings when the accumulated savings are larger. A simple way to achieve this is if a fixed proportion of accumulated savings is spent at any given time.</p>
<p>So, our consumption function now needs two parameters: the fraction of <em>income</em> that is spent at any given point in time, and the fraction of <em>savings</em> that are spent at the same time. We'll continue to use the <span class="math">\(\alpha\)</span> character, but will distinguish between the propensity to consume out of income, <span class="math">\(\alpha_Y\)</span>, and the propensity to consume out of savings, <span class="math">\(\alpha_H\)</span>. So now total consumption is the sum of spending out of both income and savings:</p>
<p><span class="math">\[C = \alpha_Y Y + \alpha_H H \hspace{1cm} (4)\]</span></p>
<p>This also means that there is an additional flow <em>out</em> of savings at any given point in time - the quantity of savings which are used for spending. So we need to update our savings adjustment equation:</p>
<p><span class="math">\[\Delta H = (1 - \alpha_Y)Y - \alpha_H H \hspace{1cm} (5)\]</span></p>
<p>We assume that the spending out of savings in any given time period is a fraction of the total accumulated savings in the <em>previous</em> time step. Thereby the discretized forms of these equations become:</p>
<p><span class="math">\[C_t = \alpha_Y Y_{t-1} + \alpha_H H_{t-1}\]</span></p>
<p><span class="math">\[H_t = H_{t-1} + (1 - \alpha_Y) Y_{t-1} - \alpha_H H_{t-1}\]</span></p>
<p>Okay, code. We'll reset the unknown variable arrays:</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[15]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="n">C</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">N</span><span class="p">)</span> <span class="c"># consumption</span>
<span class="n">Y</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">N</span><span class="p">)</span> <span class="c"># income</span>
<span class="n">H</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">N</span><span class="p">)</span> <span class="c"># private wealth</span>
</pre></div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>and define our differentiated <span class="math">\(\alpha\)</span> parameters:</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[16]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="n">alpha_y</span> <span class="o">=</span> <span class="mf">0.90</span>
<span class="n">alpha_h</span> <span class="o">=</span> <span class="mf">0.05</span>
</pre></div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>set the initial conditions again:</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[17]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="n">C</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">=</span> <span class="mi">100</span>
<span class="n">Y</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">=</span> <span class="mi">100</span>
</pre></div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>and run the model:</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[18]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="k">for</span> <span class="n">t</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">N</span><span class="p">):</span>
    <span class="n">C</span><span class="p">[</span><span class="n">t</span><span class="p">]</span> <span class="o">=</span> <span class="n">alpha_y</span> <span class="o">*</span> <span class="n">Y</span><span class="p">[</span><span class="n">t</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="o">+</span> <span class="n">alpha_h</span> <span class="o">*</span> <span class="n">H</span><span class="p">[</span><span class="n">t</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>                <span class="c"># calculate spending based on earlier income (with some saving)</span>
    <span class="n">Y</span><span class="p">[</span><span class="n">t</span><span class="p">]</span> <span class="o">=</span> <span class="n">C</span><span class="p">[</span><span class="n">t</span><span class="p">]</span>                                               <span class="c"># calculcate income earned in this time period</span>
    <span class="n">H</span><span class="p">[</span><span class="n">t</span><span class="p">]</span> <span class="o">=</span> <span class="n">H</span><span class="p">[</span><span class="n">t</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="o">+</span> <span class="p">(</span><span class="mi">1</span> <span class="o">-</span> <span class="n">alpha_y</span><span class="p">)</span> <span class="o">*</span> <span class="n">Y</span><span class="p">[</span><span class="n">t</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="o">-</span> <span class="n">alpha_h</span> <span class="o">*</span> <span class="n">H</span><span class="p">[</span><span class="n">t</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="c"># calculate change in wealth from saving and spending</span>
</pre></div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>Plot the results:</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[19]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="c"># create a figure</span>
<span class="n">fig</span> <span class="o">=</span> <span class="n">plt</span><span class="o">.</span><span class="n">figure</span><span class="p">(</span><span class="n">figsize</span><span class="o">=</span><span class="p">(</span><span class="mi">12</span><span class="p">,</span> <span class="mi">4</span><span class="p">))</span>

<span class="c"># create a subplot for consumption</span>
<span class="n">consumption_plot</span> <span class="o">=</span> <span class="n">fig</span><span class="o">.</span><span class="n">add_subplot</span><span class="p">(</span><span class="mi">131</span><span class="p">)</span>
<span class="c"># plot consumption (C) versus time step (N)</span>
<span class="n">consumption_plot</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">N</span><span class="p">),</span> <span class="n">C</span><span class="p">,</span> <span class="n">lw</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="c"># add gridlines</span>
<span class="n">consumption_plot</span><span class="o">.</span><span class="n">grid</span><span class="p">()</span>
<span class="c"># ensure a zero origin for the y axis</span>
<span class="n">consumption_plot</span><span class="o">.</span><span class="n">set_ylim</span><span class="p">([</span><span class="mi">0</span><span class="p">,</span> <span class="n">np</span><span class="o">.</span><span class="n">max</span><span class="p">(</span><span class="n">C</span><span class="p">)])</span>
<span class="c"># label axes</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">&#39;time&#39;</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">&#39;consumption&#39;</span><span class="p">)</span>

<span class="c"># create a second subplot for income</span>
<span class="n">income_plot</span> <span class="o">=</span> <span class="n">fig</span><span class="o">.</span><span class="n">add_subplot</span><span class="p">(</span><span class="mi">132</span><span class="p">)</span>
<span class="c"># plot income (Y) versus time step (N)</span>
<span class="n">income_plot</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">N</span><span class="p">),</span> <span class="n">Y</span><span class="p">,</span> <span class="n">lw</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="c"># add gridlines</span>
<span class="n">income_plot</span><span class="o">.</span><span class="n">grid</span><span class="p">()</span>
<span class="c"># ensure a zero origin for the y axis</span>
<span class="n">income_plot</span><span class="o">.</span><span class="n">set_ylim</span><span class="p">([</span><span class="mi">0</span><span class="p">,</span> <span class="n">np</span><span class="o">.</span><span class="n">max</span><span class="p">(</span><span class="n">Y</span><span class="p">)])</span>
<span class="c"># label axes</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">&#39;time&#39;</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">&#39;income&#39;</span><span class="p">)</span>

<span class="c"># create a third subplot for private wealth</span>
<span class="n">wealth_plot</span> <span class="o">=</span> <span class="n">fig</span><span class="o">.</span><span class="n">add_subplot</span><span class="p">(</span><span class="mi">133</span><span class="p">)</span>
<span class="c"># plot wealth (H) versus time step (N)</span>
<span class="n">wealth_plot</span><span class="o">.</span><span class="n">plot</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">N</span><span class="p">),</span> <span class="n">H</span><span class="p">,</span> <span class="n">lw</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
<span class="c"># add gridlines</span>
<span class="n">wealth_plot</span><span class="o">.</span><span class="n">grid</span><span class="p">()</span>
<span class="c"># ensure a zero origin for the y axis</span>
<span class="n">wealth_plot</span><span class="o">.</span><span class="n">set_ylim</span><span class="p">([</span><span class="mi">0</span><span class="p">,</span> <span class="mi">100</span><span class="p">])</span>
<span class="c"># label axes</span>
<span class="n">plt</span><span class="o">.</span><span class="n">xlabel</span><span class="p">(</span><span class="s">&#39;time&#39;</span><span class="p">)</span>
<span class="n">plt</span><span class="o">.</span><span class="n">ylabel</span><span class="p">(</span><span class="s">&#39;wealth&#39;</span><span class="p">)</span>

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
YII=
">

</div>
</div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>Like the last model, incomes initially decreased as savings begin to grow. The reason, like the last model, is that the attempt to accumulate savings reduces the stock of money circulating as spending. The difference in this model, however, is that this process is ultimately limited: incomes eventually reach a minimum level at which they remain. At the same time, the growth of savings slows down and eventually stops and the stock of accumulated savings reaches a maximum value at which it remains thereafter. We can think of our economy as comprising two distinct phases: an initial phase in which the economy is undergoing change; and an eventual non-changing phase. The latter is commonly described using the term <em>steady-state</em>.</p>
<p>So our citizens have responded to their decreasing incomes by raiding their stock of savings. As incomes dropped (<em>because</em> of the growth in accumulated savings), so the amount spent out of savings rose. At some point, the amount of money being saved out of income matched the amount of money being spent out of savings resulting in no change to the stock of accumulated savings and no further drain of money out of the spending cycle. In comparison to the last model, where the attempt to save continued <em>ad absurdum</em>, this economy has been saved from catastophe. But the steady-state balance attained in the economy represents a lower level of income than in the case where no saving is attempted. So the price (!) of saving (in this economy) is less spending and lower incomes.</p>
<p>In the last model saw that the paradox of thrift caused an uncontrollable, downward spiral into catastrophic recession. In this model we see the paradox of thrift in a slightly more nuanced form. The catastrophe of the previous model was averted only because the extent of saving was limited. Citizens, in their collective attempt to save, were forced to (partially) abandon that attempt in a bid to retain their incomes. Although some saving was acheived and some level of income was retained, the ability of the economy to save in aggregate in this model is intrisically limited by the cost it imposes on incomes.</p>
</div>
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="The-steady-state">The steady-state<a class="anchor-link" href="#The-steady-state">&#182;</a></h2>
</div>

<div class="text_cell_render border-box-sizing rendered_html">
<p>The level at which the economy settles down can be understood in terms of the spending behaviour of our citizens - the extent to which they prioritise saving over income. In order to dig in to this, we can study the steady-state phase of our model specifically. The fact that things are not changing in the steady-state phase (by definition) is a feature we can exploit to deduce some new relationships between our variables. First, we'll identify the steady-state values of our variables by using the <span class="math">\(^*\)</span> superscript. So we have <span class="math">\(C^*\)</span>, <span class="math">\(Y^*\)</span> and <span class="math">\(H^*\)</span>, which, although variable in general, are constant values in the steady-state phase. This notation helps us to remember that we are looking at a particular phase of our results. Next, let's look at the equation which determined the change in savings in our model:</p>
<p><span class="math">\[\Delta H = (1 - \alpha_Y)Y - \alpha_H H\]</span></p>
<p>At steady-state, using our <span class="math">\(^*\)</span> notation, this equation becomes:</p>
<p><span class="math">\[\Delta H^* = (1 - \alpha_Y)Y^* - \alpha_H H^*\]</span></p>
<p>But under steady-state conditions we also know that <span class="math">\(H^*\)</span> is actually not changing at all, and therefore we can equate <span class="math">\(\Delta H^*\)</span> with <span class="math">\(0\)</span>:</p>
<p><span class="math">\[0 = (1 - \alpha_Y)Y^* - \alpha_H H^*\]</span></p>
<p>and rearranging:</p>
<p><span class="math">\[(1 - \alpha_Y)Y^* = \alpha_H H^*\]</span></p>
<p>This equation simply states mathematically what we articulated earlier: that, at steady-state, the rate of saving out of income is equal to the rate of spending out of savings. Rearranging this to solve for <span class="math">\(H^*\)</span> we get:</p>
<p><span class="math">\[H^* = \frac{(1 - \alpha_Y)}{\alpha_H}Y^* \hspace{1cm} (6)\]</span></p>
<p>So the steady-state quantity of accumulated savings is directly related to the steady-state level of income. In effect, we can consider the maximum level of accumulated savings as a kind of &quot;wealth&quot; target relative to income: when the economy reaches its wealth target it is content to stay at that level and save no more. Its worth pointing out that often it is useful to measure economic metrics relative to the income of the economy (e.g. debt relative to GDP)</p>
<p>The term <span class="math">\(\frac {(1 - \alpha_Y)}{\alpha_H}\)</span> defines what this balance between wealth and income is. To make things a bit more intuitive we can think of the numerator term <span class="math">\((1 - \alpha_Y)\)</span> as the propensity to <em>save</em> (out of income). This should be quite obvious - if we subtract the propensity to <em>consume</em> from 1, we get the propensity to <em>save</em>, simply because what is not spent is saved (in this model). So the numerator and denominator can be intuitively seen as flows <em>into</em> and <em>out of</em> savings respectively, which makes the implications of the equation a bit clearer. If the flow into savings (<span class="math">\(1 - \alpha_Y\)</span>) is greater than the flow out of savings (<span class="math">\(\alpha_H\)</span>), then saving will be prioritised: the ratio will be <span class="math">\(&gt;1\)</span> and the wealth target of the economy will therefore be greater than <span class="math">\(1 \times\)</span> the steady-state income. If the spending out of savings exceeds the rate of saving from income, then the converse is true: spending will be prioritised and steady-state wealth will be less than <span class="math">\(1 \times\)</span> steady-state income.</p>
<p>Let's examine these values in our model. Our value for <span class="math">\((1 - \alpha_Y)\)</span> is:</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[20]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="k">print</span><span class="p">(</span><span class="mi">1</span> <span class="o">-</span> <span class="n">alpha_y</span><span class="p">)</span>
</pre></div>

</div>
</div>

<div class="vbox output_wrapper">
<div class="output vbox">


<div class="hbox output_area"><div class="prompt"></div>
<div class="box-flex1 output_subarea output_stream output_stdout">
<pre>
0.1

</pre>
</div>
</div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>This tells us that our economy saves 10% of income (since it spends 90%). Therefore the steady-state level of savings relative to income is:</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[21]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="k">print</span><span class="p">((</span><span class="mi">1</span> <span class="o">-</span> <span class="n">alpha_y</span><span class="p">)</span><span class="o">/</span><span class="n">alpha_h</span><span class="p">)</span>
</pre></div>

</div>
</div>

<div class="vbox output_wrapper">
<div class="output vbox">


<div class="hbox output_area"><div class="prompt"></div>
<div class="box-flex1 output_subarea output_stream output_stdout">
<pre>
2.0

</pre>
</div>
</div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>So we expect our steady-state savings to be double the value of steady-state income. Lets, see if that is true. We'll inspect the final values for income (<span class="math">\(Y\)</span>) and savings (<span class="math">\(H\)</span>) in our model results.</p>
</div>
<div class="cell border-box-sizing code_cell vbox">
<div class="input hbox">
<div class="prompt input_prompt">
In&nbsp;[22]:
</div>
<div class="input_area box-flex1">
<div class="highlight"><pre><span class="k">print</span><span class="p">(</span><span class="n">Y</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">])</span>
<span class="k">print</span><span class="p">(</span><span class="n">H</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">])</span>
</pre></div>

</div>
</div>

<div class="vbox output_wrapper">
<div class="output vbox">


<div class="hbox output_area"><div class="prompt"></div>
<div class="box-flex1 output_subarea output_stream output_stdout">
<pre>
33.3333401943
66.6666598057

</pre>
</div>
</div>

</div>
</div>

</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>Correct. Income at the end of our model was 33 pounds and total accumulated savings were double that, 66 pounds. We chose at the outset to assume that the economy saved 10% of its income (<span class="math">\(\alpha_Y = 0.90\)</span>) and spent 5% of its savings. This dictated the balance between spending and saving, and resulted in the economy desiring a stock of savings which is twice the size of its income (<span class="math">\(10/5 = 2\)</span>). If, for example, we'd set a saving out of income rate of 5% (<span class="math">\(\alpha_Y = 0.95\)</span>), we'd have found that savings would level out at the same value as income (<span class="math">\(5/5 = 1\)</span>; in this model, 50 pounds each). So, without even having to run the model explicitly, equation 6 enables us to calculate the steady-state <em>balance</em> of savings and income based on the choice of parameter values (<span class="math">\(\alpha_Y\)</span> and <span class="math">\(\alpha_H\)</span>).</p>
</div>
<div class="text_cell_render border-box-sizing rendered_html">
<p>We can reach another insight if we substitute our expression for <span class="math">\(H^*\)</span> from equation 6 into our consumption function:</p>
<p><span class="math">\[C^* = \alpha_Y Y^* + \alpha_H \frac{(1 - \alpha_Y)}{\alpha_H}Y^*\]</span></p>
<p>cancelling out <span class="math">\(\alpha_H\)</span>:</p>
<p><span class="math">\[C^* = \alpha_Y Y^* + (1 - \alpha_Y) Y^*\]</span></p>
<p>and factoring out <span class="math">\(Y^*\)</span>:</p>
<p><span class="math">\[C^* = (\alpha_Y + 1 - \alpha_Y) Y^*\]</span></p>
<p>which simplifies to:</p>
<p><span class="math">\[C^* = Y^*\]</span></p>
<p>So at steady state, spending (consumption) is equal to income. This resembles an economy without any saving at all (!): a constant, unchanging amount of money flowing through the spending cycle, simply being spent and earned, spent and earned, and leading to constant levels of income. But the difference in this scenario is two-fold. Firstly, there <em>is</em> saving happening in the steady-state phase of this economy, but just no <em>net</em> saving. The amount being saved out of income is exactly balanced with the amount being spent out of savings, so although there are flows in to and out of the stock of accumulated savings, there is no change in the size of that stock. This kind of balance is called <em>dynamic equilibrium</em>.</p>
<p>The second difference between this steady-state phase and the wholly non-saving model is that the stock of money which is ultimately circulating through the economy is now only a fraction of the whole available money stock. The ratio of savings to income shows how the total stock of money is split up. Some portion of it is held out of circulation as accumulated savings and the remainder is able to drive the circular flow of money which arises via spending. In our example, two-thirds of the money stock was eventually hoarded as accumulated savings, with the remaining one-third supporting a lower level of income. It is clear to see why, in this type of economy, saving causes a loss of incomes: there is a finite pot of money and if some is to be held aside then some must be lost from the spending cycle which produces incomes.</p>
</div>
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Conclusion">Conclusion<a class="anchor-link" href="#Conclusion">&#182;</a></h2>
</div>

<div class="text_cell_render border-box-sizing rendered_html">
<p>We tried 2 types of saving behaviour and found that in both cases, saving ended up being, to some extent, self-defeating.</p>
<p>Saving caused a build up of wealth but a reduction in incomes. This is because saved money is held out of the circular flow of money which produces incomes. Saving cannot continue indefinitely, as this would result in entire money supply being held in wealth, with no economic activty at all. A more realistic scenario is that continued attempts to save result in consumption being funded out of savings. This inherently limits the amount which can be saved. If saving is desired, our economy had to choose a balance between saving and income.</p>
<p>These results need to be considered in the correct context. Firstly, it is worth stressing that we are looking at saving and incomes on an <em>economy-wide</em> level. It is <em>not</em> necessarily true to say that the more a single individual saves, the lower <em>their individual income</em> will become. Both the spending behaviour and incomes of individuals are likely to vary across any economy and there is no direct relationship between a person's spending behaviour and their personal income. The insight of this model is that the <em>aggregate</em> spending behaviour of the entire economy <em>does</em> affect the <em>aggregate</em> income of the entire economy.</p>
<p>Secondly, these results they refer to an economy with a fixed money supply. It is specifically <em>because</em> there is no source of new money in our economy that accumulating savings necessarily means removing that money from the spending cycle. In general, saving can be considered to be a drain of money from the economy. In (the much more complex) real, modern economies, there are some mechanisms available to potentially compensate for this drainage of savings. But in a fixed money supply, greater savings necessarily cause lower aggregate incomes.</p>
</div>