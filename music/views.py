import  json
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User,AbstractUser
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect,HttpResponse,NoReverseMatch,HttpResponsePermanentRedirect,Http404,HttpResponseRedirect
from django.db.models import Q
from .forms import AlbumForm, SongForm, UserForm
from .models import Album, Song,CustomUser,FeebBack,P_Album
from django.contrib.auth.models import User
from .token import account_activation_token
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import  settings
from django.core.mail import send_mail,EmailMessage
from django.contrib import  messages

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


# ----------------- Testing ----------------------------

def testing(request):
    return render(request, 'music/unused/test.html')
def testing2(request):
    return render(request, 'music/unused/test2.html')
def testing3(request):
    return render(request, 'music/unused/test3.html')
# ----------------End Testing --------------------------



def create_album(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login_new.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_album.html', context)
            album.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, 'music/create_album.html', context)


def create_song(request, album_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login_new.html')
    else:
        # print(request.POST)
        form = SongForm(request.POST or None, request.FILES or None)
        album = get_object_or_404(Album, pk=album_id)
        if form.is_valid():
            albums_songs = album.song_set.all()
            for s in albums_songs:
                if s.song_title == form.cleaned_data.get("song_title"):
                    context = {
                        'album': album,
                        'form': form,
                        'error_message': 'You already added that song',
                    }
                    return render(request, 'music/create_song.html', context)
            song = form.save(commit=False)
            song.album = album
            song.user = request.user
            song.audio_file = request.FILES['audio_file']
            file_type = song.audio_file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in AUDIO_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Audio file must be WAV, MP3, or OGG',
                }
                return render(request, 'music/create_song.html', context)

            song.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {
            'album': album,
            'form': form,
        }
        return render(request, 'music/create_song.html', context)


def delete_album(request, album_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login_new.html')
    else:
        album = Album.objects.get(pk=album_id)
        album.delete()
        albums = Album.objects.filter(user=request.user)
        return render(request, 'music/index.html', {'albums': albums})
def delete_palbum(request, album_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login_new.html')
    else:
        album = P_Album.objects.get(pk=album_id)
        album.delete()
        albums = P_Album.objects.filter(user=request.user)
        return render(request, 'music/index_public.html', {'albums': albums})


def delete_song(request, album_id, song_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login_new.html')
    else:
        album = get_object_or_404(Album, pk=album_id)
        song = Song.objects.get(pk=song_id)
        song.delete()
        return render(request, 'music/detail.html', {'album': album})


def detail(request, album_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login_new.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/detail.html', {'album': album, 'user': user})
def detail_public(request, album_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login_new.html')
    else:
        user = request.user
        album = get_object_or_404(P_Album, pk=album_id)

        song = Song.objects.filter(album_id=album.original)
        return render(request, 'music/detail_public.html', {'album': album,'songs':song ,'user': user})

def p_album(request, album_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login_new.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        for item in CustomUser.objects.all().distinct():
            if not item.id == request.user.id:
                pp = P_Album(user = item,original=album,artist=album.artist,album_title=album.album_title,genre=album.genre,album_logo=album.album_logo,is_favorite=album.is_favorite)
                pp.save()

        return render(request, 'music/detail.html', {'album': album, 'user': user})


def favorite(request, song_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login_new.html')
    else:
        song = get_object_or_404(Song, pk=song_id)
        try:
            if song.is_favorite:
                song.is_favorite = False
            else:
                song.is_favorite = True
            song.save()
        except (KeyError, Song.DoesNotExist):
            return JsonResponse({'success': False})
        else:
            return JsonResponse({'success': True})


def favorite_album(request, album_id):
    if not request.user.is_authenticated:
        return render(request, 'music/login_new.html')
    else:
        album = get_object_or_404(Album, pk=album_id)
        try:
            if album.is_favorite:
                album.is_favorite = False
            else:
                album.is_favorite = True
            album.save()
        except (KeyError, Album.DoesNotExist):
            return JsonResponse({'success': False})
        else:
            return JsonResponse({'success': True})



def songs(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'music/login_new.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user_id=request.user.id):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })






def index(request):
    if not request.user.is_authenticated:
        return render(request, 'music/home.html')
    else:

        albums  = Album.objects.filter(user=request.user)
        song_results = Song.objects.filter(user_id=request.user)
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'albums': albums,
                'songs': song_results,
            })
        else:
            return render(request, 'music/index.html', {'albums': albums})


def index2(request):
    if not request.user.is_authenticated:
        return render(request, 'music/home.html')
    else:
        albums  = P_Album.objects.filter(user=request.user)
        return render(request, 'music/index_public.html', {'albums': albums})






def feed(request):

    if request.method == "POST":

        tname = request.POST.get('fname')
        print(tname)
        tuseremail = request.POST.get('email')
        tphone = request.POST.get('phone')
        tmessage = request.POST.get('message')
        ff = FeebBack(name=tname, email=tuseremail, mobile_no=tphone, tmessage=tmessage)
        ff.save()

        # System to user
        mail_subject = "Thank you for your feedback"
        message = render_to_string('music/feed.html', {
            'name': tname,
        })
        from_email = settings.EMAIL_HOST_USER
        to_email = tuseremail
        to_list = [to_email]
        send_mail(mail_subject, message, from_email, to_list, fail_silently=True)


        # System to admin
        mail_subject = "User Request"
        message = render_to_string('music/feed3.html', {
            'user' : tname,
            'user_email':tuseremail,
            'tphone':tphone,
            'messg': tmessage,
        })
        from_email = settings.EMAIL_HOST_USER
        to_email = settings.EMAIL_HOST_USER
        to_list = [to_email]
        send_mail(mail_subject, message, from_email, to_list, fail_silently=True)

        return render(request, 'music/home.html')
    else:
        return render(request,'music/home.html')










# User Authentication start

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login_new.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login_new.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login_new.html')

def logout_user(request):
    auth_logout(request)
    return render(request, 'music/home.html')


def register(request):
    if request.method == 'POST':
        tusername = request.POST.get('username')
        tuseremail = request.POST.get('email')
        tpassword = request.POST.get('pass')
        user = CustomUser(username=tusername, email=tuseremail, is_superuser=False,is_staff=False, last_login=None)
        user.set_password(tpassword)
        user.is_active = False
        user.save()

        site = request.META['HTTP_HOST']
        mail_subject = "Confirmation message for MusicBox"
        message = render_to_string('music/confirm_email.html',{
            'user':user,
            'domain' : site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })

        from_email = settings.EMAIL_HOST_USER
        to_email = request.POST.get('email')



        to_list = [to_email]
        send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
        return render(request,'music/before_confirm.html')
    else:
        return render(request, 'music/reg_new.html')



def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        # return redirect('home')
        return render(request,'music/after_confirm.html')
    else:
        return HttpResponse("<h2>Activation link is invalid...! <a href='/register'> Return</a>  to the register page.</h2>")





