clear all
iteration=3000;
x=zeros(3,1);%3个输入层节点
net=zeros(5,1);%5个隐含层节点净输入
I=zeros(5,1);
y=zeros(iteration,1);%一个输出节点，但可以保存2000个循环数据
d=zeros(iteration,1);%导师数据
e=zeros(iteration,1);
u=zeros(iteration,1);
%for i=1:iteration       %设定输入值
%   u(i,1)=sin(2*pi*i/250);
%end
u(1,1)=sin(2*pi/250);
for k=2:iteration-1         %求出导师信号
    u1=sin(2*pi*k/250);
    u(k,1)=u1;
    l=0.6*sin(pi*u1)+0.3*sin(3*pi*u1)+0.1*sin(5*pi*u1);
    h=0.3*d(k,1)+0.6*d(k-1,1)+l;
    d(k+1,1)=h;
end
v=rand(3,5)*0.2-0.1;%设定权值矩阵
p=rand(1,5)*0.2-0.1;
delta_v=zeros(3,5);
delta_p=zeros(1,5);
v_temp=zeros(3,5);
p_temp=zeros(1,5);
amax=0.08;  %学习率
amin=0.001;
for Iter=1:50
    for k=2:iteration-1
        x(1,1)=y(k,1);
        x(2,1)=y(k-1,1);
        x(3,1)=u(k);
      % d(k+1,1)=Disum(x);%求出导师信号
        net=(x'*v)';%隐含单元净输入
      % I=Sig(net);
        for m=1:5
            I(m,1)=(1-exp(-net(m,1)))/(1+exp(-net(m,1)));
        end
        y(k+1,1)=p*I;
        e(k+1,1)=d(k+1,1)-y(k+1,1);
        a=amax-k/iteration*(amax-amin);
    %    p_temp=a*e*I'+a*delta_p;
     %  v_temp=a*e*0.5*(1-I.*I).*p'*x'+a*delta_v;
     %   v_temp=a*e*0.5*(1-I.*I).*p'*x'+a*delta_v;
      %  delta_p=p_temp;
       % delta_v=v_temp;
        for i=1:5
            for j=1:3
                v_temp(j,i)=a*e(k+1,1)*0.5*(1-I(i,1)^2)*p(1,i)*x(j,1)+a*delta_v(j,i);
            end
        end
        v=v+v_temp;
        delta_v=v_temp;
        p_temp=a*e(k+1,1)*I'+a*delta_p;
        p=p+p_temp;
        delta_p=p_temp;
    end
end
figure(1)
hold on
plot(d,'.');
plot(y,'r-');
figure(2)
plot(e,'b-');

