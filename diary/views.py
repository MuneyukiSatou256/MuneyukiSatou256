from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.utils import timezone
from .forms import DiaryForm,AccountForm,AccountForm_image
from django.urls import reverse_lazy
from .models import diary_table
from django.template.context_processors import request
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Create your views here.
class IndexView(TemplateView):
    template_name="index.html"
    
#createviewはformを組み込んだ画面を使用する際に使用する。
class DiaryCreateView(CreateView):
    template_name = 'diary_create.html'
    form_class=DiaryForm
    
    success_url=reverse_lazy('diary:diary_create_complete')
    
    def form_valid(self,form):
        user_obj = User.objects.get(id=self.request.user.id)
        form.instance.user = user_obj
        return super(DiaryCreateView, self).form_valid(form)
    
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['tag_list'] = Tag.objects.all
    #     return context
    
    
class DiaryCreateCompleteView(TemplateView):
    template_name='diary_create_complete.html'
    
    

#@method_decorator(login_required, name='dispatch')
class DiaryListView(ListView):
    template_name = 'diary_list.html'
    model = diary_table
    
    #get関数の引数でパラメータ取得できる。
    def get(self,request,num=1):
        
        # num =self.kwargs['num'] 
        
        
        msgs = diary_table.objects.filter(user_id=self.request.user.id)
        page = Paginator(msgs,8)
        
        params = {
            'diary_table_list':page.page(num),
            'login_user':request.user,
            'contents':page.get_page(num),
            'page': page.page_range,# list
            'page_active': num,        # intデータ
            'page_last': page.num_pages  # intデータ
            }
        
        return render(request,'diary_list.html',params)
    #
    # paginate_by = 4
    #
    # def get_queryset(self):
    #     diary_list = diary_table.objects.filter(user_id=self.request.user.id)
    #     print("-------------------------"+str(self.request.user.id))
    #     return diary_list
    
    
class DiaryDetailView(DetailView):
    template_name='diary_detail.html'
    model=diary_table

class DiaryUpdateView(UpdateView):
    template_name="diary_update.html"
    model = diary_table
    fields = ('date','title','text')
    success_url = reverse_lazy("diary:diary_list")
    
    def form_valid(self,form):
        diary=form.save(commit=False)
        diary.updated_at = timezone.now()
        diary.save()
        return super().form_valid(form)

class DiaryDeleteView(DeleteView):
    template_name = 'diary_delete.html'
    model = diary_table
    success_url = reverse_lazy('diary:diary_list')
    
class diary_register(TemplateView):
    def __init__(self):
        self.params={
            "AccountCreate":False,
            "account_form":AccountForm(),
            }
    
    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["AccountCreate"] = False
        self.params["account_form_image"] = AccountForm_image()
        
        return render(request,"diary_register.html",context=self.params)
    
    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["account_form_image"] = AccountForm_image(data=request.POST)
        
        if self.params["account_form"].is_valid() and self.params["account_form_image"]:    
            account = self.params["account_form"].save()
            account.set_password(account.password)
            account.save()
            
            #saveを実行した後は保存したモデルオブジェクトが返り値として返ってくる
            account_image = self.params["account_form_image"].save(commit=False)
            account_image.user = account
            
            if "profile_image" in request.FILES:
                account_image.profile_image = request.FILES["profile_image"]
                
            account_image.save()
            
            self.params["AccountCreate"] = True
        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)
            
        return render(request,"diary_register.html",context=self.params)
        
def Login(request):
    if request.method == 'POST':
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')
        
        user = authenticate(username=ID,password=Pass)
        
        #use = get_user_model()
        #print(use.objects.get(id=1).password)
        
        if user is not None:
            if user.is_active:
                login(request,user)
                print("ログイン成功")
                return HttpResponseRedirect(reverse('diary:diary_list'))
            else:
                return HttpResponse("アカウントが有効ではありません")
        
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    else:
        return render(request,'diary_login.html')
    
@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('diary:Login'))

    